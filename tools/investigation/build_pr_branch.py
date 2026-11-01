"""Build a pull-request branch for the author's repository (his layout: the mod at the top level; his line-ending setting):
replay package commits one by one on a fresh clone of his main, and check after each that his tree equals the package's mod/
at that commit, ignoring line endings. Prints the old -> new commit mapping. Nothing is pushed.

Usage: python tools/investigation/build_pr_branch.py <clone folder> <new branch> <package commit> [<package commit> ...]
A message file tools/investigation/out/pr_message_<commit>.txt, if it exists, replaces that commit's message."""
import os
import subprocess
import sys

PKG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUTHOR = "https://github.com/gastav3/Hoi4_1944.git"


def run(args, cwd, check=True, text=True):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=text, encoding="utf-8" if text else None)
    if check and r.returncode:
        raise SystemExit(f"{args}: {r.stderr}")
    return r.stdout


clone, branch, commits = os.path.abspath(sys.argv[1]), sys.argv[2], sys.argv[3:]
if os.path.exists(clone):
    raise SystemExit(f"{clone} exists: use a new folder")
run(["git", "clone", "-q", "--branch", "main", AUTHOR, clone], PKG)
run(["git", "checkout", "-q", "-b", branch], clone)


def tree_matches(commit):
    """Every file of the package's mod/ at this commit against the clone's working tree, ignoring CR."""
    names = run(["git", "ls-tree", "-r", "--name-only", commit, "--", "mod"], PKG).splitlines()
    bad = []
    for n in names:
        rel = n[4:].strip('"')
        p = os.path.join(clone, rel)
        if rel == ".gitattributes":  # his repository keeps its own line-ending setting (CHANGELOG section 13)
            continue
        if not os.path.exists(p):
            bad.append("missing " + rel)
            continue
        a = subprocess.run(["git", "show", f"{commit}:{n}"], cwd=PKG, capture_output=True).stdout.replace(b"\r\n", b"\n")
        b = open(p, "rb").read().replace(b"\r\n", b"\n")
        if a != b:
            bad.append("differs " + rel)
    theirs = run(["git", "ls-files"], clone).splitlines()
    extra = [t for t in theirs if t.strip('"') not in {n[4:].strip('"') for n in names} and t not in ("README.md", ".gitattributes")]
    return bad, extra


for c in commits:
    rows = run(["git", "diff", "--name-status", f"{c}^", c, "--", "mod"], PKG).splitlines()
    for row in rows:
        st, path = row.split("\t", 1)
        rel = path[4:].strip('"')
        dst = os.path.join(clone, rel)
        if st.startswith("D"):
            run(["git", "rm", "-q", "--", rel], clone)
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            data = subprocess.run(["git", "show", f"{c}:{path.strip(chr(34))}"], cwd=PKG, capture_output=True).stdout
            open(dst, "wb").write(data)
            run(["git", "add", "--", rel], clone)
    msg_file = os.path.join(PKG, "tools", "investigation", "out", f"pr_message_{c}.txt")
    msg = msg_file if os.path.exists(msg_file) else None
    if msg is None:
        msg = os.path.join(clone, ".git", "PR_MSG")
        open(msg, "w", encoding="utf-8", newline="\n").write(run(["git", "log", "-1", "--format=%B", c], PKG))
    author = run(["git", "log", "-1", "--format=%an <%ae>", c], PKG).strip()
    run(["git", "commit", "-q", "-F", msg, f"--author={author}"], clone)
    new = run(["git", "rev-parse", "HEAD"], clone).strip()
    bad, extra = tree_matches(c)
    print(f"{c} -> {new[:7]}  files {len(rows)}  tree equals the package ignoring line endings: {not bad}  {bad[:5]}  extra in his tree: {extra[:5]}")
    stats = run(["git", "show", "--stat", "--format=", "HEAD"], clone).strip().splitlines()[-1]
    print("   ", stats)
crlf = run(["git", "ls-files", "--eol"], clone).splitlines()
print("text files stored with CRLF in his repository:", sum(1 for l in crlf if l.startswith("i/crlf")))
