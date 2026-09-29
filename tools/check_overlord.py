"""Evaluate the actual Overlord decision gates against regression scenarios.

This small evaluator covers only the triggers used by these decisions. It
rejects unfamiliar syntax instead of assuming that a trigger succeeds.
It does not simulate HOI4's naval AI or prove that a landing wins.
"""
from datetime import date
from pathlib import Path
import copy
import pdx


def child(block, key):
    return next(n for n in block if n.key == key)


def decisions(text):
    tree, problems = pdx.parse(text)
    if problems:
        raise ValueError(problems)
    return {n.key: n.value for cat in tree for n in cat.value if n.is_block()}


def evaluate(block, world, scope, variables=None):
    variables = {} if variables is None else variables

    def test(n):
        key, value = n.key, n.value
        if key in ('OR', 'AND', 'NOT'):
            values = [test(c) for c in value]
            return any(values) if key == 'OR' else (not any(values) if key == 'NOT' else all(values))
        if key in world['countries'] or key.isdigit():
            return evaluate(value, world, key, variables)
        if key == 'date':
            other = date(*map(int, value.split('.')))
            return {'>': world['date'] > other, '<': world['date'] < other}[n.op]
        if key in ('set_temp_variable', 'modulo_temp_variable'):
            entry = value[0]
            number = world['num_days'] if entry.value == 'global.num_days' else int(entry.value)
            variables[entry.key] = number if key == 'set_temp_variable' else variables[entry.key] % number
            return True
        if key == 'check_variable':
            entry = value[0]
            assert entry.op == '<'
            return variables[entry.key] < float(entry.value)
        if key == 'is_fully_controlled_by':
            return world['states'][scope] == value
        country = world['countries'][scope]
        if key == 'tag':
            return scope == value
        if key in ('is_ai', 'has_capitulated'):
            return country[key] == (value == 'yes')
        if key == 'has_war_with':
            return value in country['wars']
        if key == 'has_decision':
            return value in country['decisions']
        if key == 'surrender_progress':
            assert n.op == '<'
            return country[key] < float(value)
        if key == 'controls_state':
            return world['states'][value] == scope
        raise ValueError('Unsupported trigger: ' + str(n))

    return all(test(n) for n in block)


def scenarios(text):
    definitions = decisions(text)
    prep = definitions['operation_overlord_prep']
    launch = definitions['operation_overlord']
    world = {
        'date': date(1944, 5, 30), 'num_days': 100,
        'states': {'15': 'GER', '16': 'GER'},
        'countries': {
            tag: {'is_ai': True, 'has_capitulated': False, 'wars': {'GER'},
                  'decisions': set(), 'surrender_progress': 0.0}
            for tag in ('ENG', 'USA', 'CAN', 'GER')
        },
    }
    rows = []

    def run(name, decision, keys, expected, change=lambda w: None, tag='ENG'):
        current = copy.deepcopy(world)
        change(current)
        actual = all(evaluate(child(decision, key).value, current, tag) for key in keys)
        rows.append((name, actual == expected))

    def when(day):
        return lambda w: w.update(date=date(*day))

    for day, expected in (((1944, 5, 1), False), ((1944, 5, 2), True),
                          ((1944, 5, 28), True), ((1944, 5, 29), False),
                          ((1944, 6, 1), False), ((1945, 5, 2), False)):
        run('prep available on ' + str(day), prep, ('allowed', 'visible', 'available'), expected, when(day))
    if any(n.key == 'cancel_trigger' for n in prep):
        run('prep stays active before cutoff', prep, ('cancel_trigger',), False, when((1944, 5, 28)))
        run('prep cancels on May 29', prep, ('cancel_trigger',), True, when((1944, 5, 29)))
        run('active launch cancels prep', prep, ('cancel_trigger',), True,
            lambda w: (w.update(date=date(1944, 5, 28)), w['countries']['ENG']['decisions'].add('operation_overlord')))
        run('peace cancels prep', prep, ('cancel_trigger',), True,
            lambda w: (w.update(date=date(1944, 5, 28)), w['countries']['ENG']['wars'].clear()))
    else:
        rows.append(('prep has a cancellation condition', False))
    keys = ('allowed', 'visible', 'available')
    run('launch blocked before window', launch, keys, False, when((1944, 5, 29)))
    run('launch opens on May 30', launch, keys, True)
    run('launch closes on November 1', launch, keys, False, when((1944, 11, 1)))
    for tag in ('ENG', 'USA'):
        run(tag + ' can launch after minor British losses', launch, keys, True,
            lambda w: w['countries']['ENG'].update(surrender_progress=0.02), tag)
        run(tag + ' can launch after minor American losses', launch, keys, True,
            lambda w: w['countries']['USA'].update(surrender_progress=0.02), tag)
        run(tag + ' capitulation blocks launch', launch, keys, False,
            lambda w, tag=tag: w['countries'][tag].update(has_capitulated=True))
    run('human UK unaffected', launch, keys, False, lambda w: w['countries']['ENG'].update(is_ai=False))
    run('Canada still has no launch decision', launch, keys, False, tag='CAN')
    run('peace blocks launch', launch, keys, False, lambda w: w['countries']['ENG']['wars'].clear())
    run('existing Normandy foothold blocks repeat boost', launch, keys, False, lambda w: w['states'].update({'15': 'USA'}))
    run('liberated Paris blocks launch', launch, keys, False, lambda w: w['states'].update({'16': 'FRA'}))
    run('original rest-day gate preserved', launch, keys, False, lambda w: w.update(num_days=88))
    return rows


def calibration(text):
    """Restore each defect separately; the scenario suite must reject it."""
    candidates = {
        'late preparation': text.replace('date < 1944.5.29', 'date < 1945.5.10', 1),
        'late cancellation': text.replace('date > 1944.5.28', 'date > 1945.5.28', 1),
        'one-percent British gate': text.replace('ENG = { has_capitulated = no }', 'ENG = { surrender_progress < 0.01 }', 1),
        'one-percent American gate': text.replace('USA = { has_capitulated = no }', 'USA = { surrender_progress < 0.01 }', 1),
    }
    return [(name, changed != text and not all(ok for _, ok in scenarios(changed)))
            for name, changed in candidates.items()]


if __name__ == '__main__':
    source = Path('mod/common/decisions/Allies_1944.txt').read_text(encoding='utf-8-sig')
    results = scenarios(source) + [('reject planted ' + name, ok) for name, ok in calibration(source)]
    for name, ok in results:
        print(('PASS ' if ok else 'FAIL ') + name)
    print(f'{sum(ok for _, ok in results)}/{len(results)} passed')
    raise SystemExit(0 if all(ok for _, ok in results) else 1)
