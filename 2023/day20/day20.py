from collections import defaultdict, deque
import re
from aoc_utils import * # type: ignore
from aocd import get_data

from dataclasses import dataclass

class Module:
    name: str
    destinations: list[str]

    def pulse(self, source: str, signal: bool) -> list[tuple[bool, str]]:
        ...

    def send(self, signal) -> list[tuple[str, str, bool]]:
        return [(self.name, dst, signal) for dst in self.destinations]


@dataclass
class FlipFlop(Module):
    name: str
    destinations: list[str]
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
    destinations: list[str]

    def pulse(self, source: str, signal: bool) -> list[tuple[str, str, bool]]:
        self.inputs[source] = signal
        return self.send(not all(self.inputs.values()))

@dataclass
class Broadcast(Module):
    name: str
    destinations: list[str]

    def pulse(self, source: str, signal: bool) -> list[tuple[str, str, bool]]:
        return self.send(signal)

BROADCASTER = "broadcaster"

def parse_modules(data):
    modules = {}

    mapping = defaultdict(list)
    for line in data.splitlines():
        if match := re.match(r"%(.*) -> (.*)", line):
            name, d = match.groups()
            destinations = d.split(", ")
            modules[name] = FlipFlop(name, destinations)
            mapping[name].extend(destinations)
        elif match := re.match(r"&(.*) -> (.*)", line):
            name, d = match.groups()
            destinations = d.split(", ")
            modules[name] = Conjunction(name, {}, destinations)
            mapping[name].extend(destinations)
        elif match := re.match(r"broadcaster -> (.*)", line):
            d = match.group(1)
            destinations = d.split(", ")
            modules[BROADCASTER] = Broadcast(BROADCASTER, destinations)
            mapping[BROADCASTER].extend(destinations)

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

data = get_data(year=2023, day=20, block=True)

print(part_one(data))
