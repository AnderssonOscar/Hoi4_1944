"""Structural checks over every script file in the mod.

  * unbalanced braces            - a '{' never closed, or an extra '}'
  * division template slot clash - two regiments / support companies given
                                   the same x/y position in one template

(An `else` written inside its `if` block is valid HOI4 syntax; vanilla does it
182 times, so this script deliberately does not flag it.)

Usage:  python tools/check_structure.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pdx  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(HERE, "..", "mod")


def files():
    for sub in ("common", "events", "history"):
        for dirpath, _, names in os.walk(os.path.join(MOD, sub)):
            for f in names:
                if f.endswith(".txt"):
                    yield os.path.join(dirpath, f)


def check_templates(root, rel, out):
    for node, _ in pdx.walk(root):
        if node.key != "division_template" or not node.is_block():
            continue
        name = next((c.value for c in node.value if c.key == "name"), "?")
        for section in ("regiments", "support"):
            sec = next((c for c in node.value if c.key == section and c.is_block()), None)
            if not sec:
                continue
            seen = {}
            for unit in sec.value:
                if not unit.is_block():
                    continue
                x = next((c.value for c in unit.value if c.key == "x"), None)
                y = next((c.value for c in unit.value if c.key == "y"), None)
                if (x, y) in seen:
                    out.append(f"{rel}:{unit.line}  template {name}: {section} slot x={x} y={y} used twice"
                               f" ({seen[(x, y)]} and {unit.key})")
                else:
                    seen[(x, y)] = unit.key


def main():
    braces, templates = [], []
    count = 0
    for path in files():
        count += 1
        rel = os.path.relpath(path, MOD).replace("\\", "/")
        root, problems = pdx.parse_file(path)
        braces += [f"{rel}:{line}  {msg}" for line, msg in problems]
        check_templates(root, rel, templates)
    print(f"Checked {count} script files\n")
    for title, items in (("Unbalanced braces", braces),
                         ("Division template slot clashes", templates)):
        print(f"== {title} ({len(items)}) ==")
        for i in items:
            print("  " + i)
        print()


if __name__ == "__main__":
    main()
