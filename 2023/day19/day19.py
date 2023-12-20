import re
from aoc_utils import *
from aocd import get_data

LT = True
GT = False

from dataclasses import dataclass

@dataclass(frozen=True)
class Workflow:
    rules: list[tuple]
    default: str

def parse_workflows(data):
    workflows_spec, parts_spec = data.split('\n\n')
    workflows = {}
    parts = [ints(l) for l in parts_spec.splitlines()]
    for line in workflows_spec.splitlines():
        rules = []
        if match := re.match(r"(.*){(.*)}", line):
            name, rules_spec = match.groups()
            checks = rules_spec.split(",")
            for rule in checks[:-1]:
                if m := re.match(r"(x|m|a|s)([])(\d+):(.*)", rule):
                    prop, cmp, limit, result = m.groups()
                    rules.append(('xmas'.index(prop), cmp == '<', int(limit), result))
                else:
                    assert False
            
            workflows[name] = Workflow(rules, default=checks[-1])
        else:
            assert False


    return workflows, parts

def eval_workflow(workflow, part):
    for (i, op, limit, res) in workflow.rules:
        value = part[i]
        if op is LT and value < limit:
            return res
        elif op is GT and value > limit:
            return res

    return workflow.default


def part_one(data):
    workflows, parts = parse_workflows(data)
    accepted = []
    for part in parts:
        res = "in"

        while res != 'A' and res != 'R':
            res = eval_workflow(workflows[res], part)

        if res == 'A':
            accepted.append(part)

    return sum(sum(part) for part in accepted)


def explore_workflow(workflow, constraints):
    for (i, op, limit, res) in workflow.rules:
        l, r = constraints[i]

        if op is LT and l < limit:
            new_range = (l, min(limit, r))
            constraints[i] = (min(limit, r), r)
            cons = constraints[:i] + [new_range] + constraints[i+1:]

            yield (res, cons)

            if limit >= r:
                return
        elif op is GT and r > limit:

            new_range = (max(l, limit+1), r)
            constraints[i] = (l, max(l, limit+1))
            cons = constraints[:i] + [new_range] + constraints[i+1:]

            yield (res, cons)

            if limit <= l:
                return

    yield (workflow.default, constraints)


def part_two(data):
    workflows, _ = parse_workflows(data)
    queue = [(workflows["in"], [(1, 4001), (1, 4001), (1, 4001), (1, 4001)])]
    accepted = 0
    while queue:
        workflow, constraints = queue.pop()
        for res, cons in explore_workflow(workflow, constraints):
            if res == 'A':
                s = 1
                for (l, r) in cons:
                    s *= (r - l)
                accepted += s
            elif res != 'R':
                queue.append((workflows[res], cons))

    return accepted

data = get_data(year=2023, day=19, block=True)

print(part_one(data))
print(part_two(data))
