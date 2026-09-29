"""Exercise the recovered daily D-Day script with small territorial scenarios.

Only the triggers/effects present in this script are implemented. Unknown
syntax is an error. This verifies event logic, not combat or naval AI.
"""
from datetime import date, timedelta
from pathlib import Path
import pdx


def block(nodes, name):
    return next(n.value for n in nodes if n.key == name)


def coast_map():
    result = {}
    for sid in ('15', '14', '29', '6'):
        path = next(p for p in Path('mod/history/states').iterdir() if p.name.split('-')[0].strip() == sid)
        state = block(pdx.parse_file(path)[0], 'state')
        result[sid] = [n.value for n in block(state, 'provinces')]
    return result


class World:
    def __init__(self, coast):
        self.coast = coast
        self.controllers = {p: 'GER' for ps in coast.values() for p in ps}
        self.date = date(1944, 6, 1)
        self.flags = set()
        self.events = []
        self.enemies = {'ENG', 'USA', 'FRA', 'SOV'}
        self.factions = {'GER': 'axis', 'ITA': 'axis', 'ENG': 'allies',
                         'USA': 'allies', 'FRA': 'allies', 'SOV': 'comintern', 'SWE': 'neutral'}

    def test(self, nodes, scope='GER'):
        def node(n):
            key, value = n.key, n.value
            if key in ('OR', 'AND', 'NOT'):
                values = [node(c) for c in value]
                return any(values) if key == 'OR' else (not any(values) if key == 'NOT' else all(values))
            if key in ('any_enemy_country', 'any_country'):
                countries = self.enemies if key == 'any_enemy_country' else self.factions
                return any(self.test(value, tag) for tag in countries)
            if key.isdigit():
                return self.test(value, key)
            if key == 'date':
                assert n.op == '>'
                return self.date > date(*map(int, value.split('.')))
            if key == 'has_country_flag':
                return value in self.flags
            if key == 'has_war_with':
                assert scope == 'GER'
                return value in self.enemies
            if key == 'tag':
                return scope == value
            if key == 'is_in_faction_with':
                return self.factions[scope] == self.factions[value]
            if key == 'controls_province':
                return self.controllers.get(value) == scope
            if key == 'is_fully_controlled_by':
                tag = 'GER' if value == 'ROOT' else value
                return all(self.controllers[p] == tag for p in self.coast[scope])
            if key == 'always':
                return value == 'yes'
            raise ValueError('Unsupported trigger: ' + str(n))
        return all(node(n) for n in nodes)

    def tick(self, effects):
        for effect in effects:
            assert effect.key == 'if'
            if self.test(block(effect.value, 'limit')):
                for n in effect.value:
                    if n.key == 'limit':
                        continue
                    if n.key == 'set_country_flag':
                        self.flags.add(n.value)
                    elif n.key == 'country_event':
                        data = {c.key: c.value for c in n.value}
                        self.events.append((data['id'], self.date + timedelta(days=int(data.get('days', '0')))))
                    else:
                        raise ValueError('Unsupported effect: ' + str(n))


def scenarios(text):
    tree, problems = pdx.parse(text)
    assert not problems, problems
    effects = block(block(block(tree, 'on_actions'), 'on_daily_GER'), 'effect')
    coast = coast_map()
    first = next(iter(coast.values()))[0]
    results = []
    for invader, expected in (('ENG', True), ('USA', True), ('FRA', True),
                              ('ITA', False), ('SOV', False), ('SWE', False)):
        world = World(coast)
        world.controllers[first] = invader
        world.tick(effects)
        results.append((invader + ' landing classification', ('GER_dday_landed' in world.flags) == expected and not world.events))
    world = World(coast)
    world.date = date(1944, 5, 31)
    world.controllers[first] = 'ENG'
    world.tick(effects)
    results.append(('no event before June', not world.flags and not world.events))
    world = World(coast)
    world.enemies.remove('USA')
    world.controllers[first] = 'USA'
    world.tick(effects)
    results.append(('non-enemy USA cannot count as landing', not world.flags))
    for province in world.controllers:
        sample = World(coast)
        sample.controllers[province] = 'ENG'
        sample.tick(effects)
        results.append(('partial beachhead in province ' + province, 'GER_dday_landed' in sample.flags))
    world = World(coast)
    world.tick(effects)
    results.append(('no celebration without prior landing', not world.flags and not world.events))
    world.controllers[first] = 'ENG'
    world.tick(effects)
    world.date += timedelta(days=1)
    world.tick(effects)
    results.append(('no celebration while beachhead survives', not world.events))
    world.controllers[first] = 'GER'
    world.tick(effects)
    results.append(('celebration scheduled one day after recapture', world.events == [('ger_dday.1', world.date + timedelta(days=1))]))
    world.date += timedelta(days=1)
    world.tick(effects)
    world.controllers[first] = 'ENG'
    world.tick(effects)
    world.controllers[first] = 'GER'
    world.tick(effects)
    results.append(('second landing cannot repeat celebration', len(world.events) == 1))
    return results


def calibration(text):
    first = next(iter(coast_map().values()))[0]
    mutants = {
        'non-enemy occupation': text.replace('any_enemy_country = {', 'any_country = {', 1),
        'missing coastal province': text.replace('controls_province = ' + first, 'controls_province = 999999', 1),
        'no one-day delay': text.replace('days = 1', 'days = 0', 1),
    }
    return [(name, altered != text and not all(ok for _, ok in scenarios(altered))) for name, altered in mutants.items()]


if __name__ == '__main__':
    text = Path('mod/common/on_actions/GER_dday_on_actions.txt').read_text(encoding='utf-8')
    results = scenarios(text) + [('reject planted ' + name, ok) for name, ok in calibration(text)]
    for name, ok in results:
        print(('PASS ' if ok else 'FAIL ') + name)
    print(f'{sum(ok for _, ok in results)}/{len(results)} passed')
    raise SystemExit(0 if all(ok for _, ok in results) else 1)
