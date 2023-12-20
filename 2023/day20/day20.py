from collections import defaultdict, deque
import re

from aoc_utils import *
from aocd import get_data

from dataclasses import dataclass

class Module:
    name: str
    outputs: list[str]

    def pulse(self, source: str, signal: bool) -> list[tuple[bool, str]]:
        ...

    def send(self, signal) -> list[tuple[str, str, bool]]:
        return [(self.name, dst, signal) for dst in self.outputs]


@dataclass
class FlipFlop(Module):
    name: str
    outputs: list[str]
    state: bool = False

    def pulse(self, source: str, signal: bool) -> list[tuple[str, str, bool]]:
        if not signal:
            self.state = not self.state
            return self.send(self.state)
        return []

@dataclass
class Conjunction(Module):
    name: str
    inputs: dict[str, bool]
    outputs: list[str]

    def pulse(self, source: str, signal: bool) -> list[tuple[str, str, bool]]:
        self.inputs[source] = signal
        return self.send(not all(self.inputs.values()))

@dataclass
class Broadcast(Module):
    name: str
    outputs: list[str]

    def pulse(self, source: str, signal: bool) -> list[tuple[str, str, bool]]:
        return self.send(signal)

BROADCASTER = "broadcaster"

def parse_modules(data):
    modules = {}

    mapping = defaultdict(list)
    for line in data.splitlines():
        if match := re.match(r"%(.*) -> (.*)", line):
            name, d = match.groups()
            outputs = d.split(", ")
            modules[name] = FlipFlop(name, outputs)
            mapping[name].extend(outputs)
        elif match := re.match(r"&(.*) -> (.*)", line):
            name, d = match.groups()
            outputs = d.split(", ")
            modules[name] = Conjunction(name, {}, outputs)
            mapping[name].extend(outputs)
        elif match := re.match(r"broadcaster -> (.*)", line):
            d = match.group(1)
            outputs = d.split(", ")
            modules[BROADCASTER] = Broadcast(BROADCASTER, outputs)
            mapping[BROADCASTER].extend(outputs)

    for name, module in modules.items():
        if isinstance(module, Conjunction):
            for (src, dsts) in mapping.items():
                if name in dsts:
                    module.inputs[src] = False
    return modules

def part_one(data):
    modules = parse_modules(data)
    pulses = deque()
    counts = [0, 0]
    for i in range(1000):
        pulses.append((None, BROADCASTER, False))

        while pulses:
            src, dst, signal = pulses.popleft()
            if dst in modules:
                pulses.extend(modules[dst].pulse(src, signal))
            counts[signal] += 1

    return counts[0]*counts[1]

from math import lcm

def part_two(data):
    modules = parse_modules(data)

    # From manual inspection - rx has a single conjunction input
    rx_input = next(module for module in modules.values() if module.outputs == ['rx'])
    cycles = { name: None for name in rx_input.inputs }

    i = 0
    pulses = deque()

    while not all(cycles.values()):
        i += 1
        pulses.append((None, BROADCASTER, False))

        while pulses:
            src, dst, signal = pulses.popleft()
            if dst in modules:
                pulses.extend(modules[dst].pulse(src, signal))

            # find out how many presses until each input of the conjunction emits a high signal
            if src in cycles and signal:
                cycles[src] = i

    # assume the whole thing is periodic with no offsets to make it complicated
    # they all emit high signals at the LCM
    return lcm(*cycles.values())

data = get_data(year=2023, day=20, block=True)

print(part_one(data))
print(part_two(data))
