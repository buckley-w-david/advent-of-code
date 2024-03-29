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

def graphviz(data):
    print("digraph G {")
    for line in data.splitlines():
        if line.startswith("broadcaster"):
            print(" ", line + ";")
        else:
            print(" ", line[1:] + ";")
    print("}")

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

def part_two_no_eval(data):
    modules = parse_modules(data)

    # From manual inspection - rx has a single conjunction input
    rx_input = next(module for module in modules.values() if module.outputs == ['rx'])

    # This single input is fed by a series of modules
    outputs = [ modules[name] for name in rx_input.inputs ]

    # That each have a single input to a "hub"
    hubs = { name for mod in outputs for name in mod.inputs }

    # Each hub collects the outputs of a chain of FlipFlops that form a counter
    # We can extract what number the counter is counting towrads by analysing the chain

    # The BROADCASTER module connects to the first module in the chains around the hubs
    chain_start = modules[BROADCASTER].outputs

    cycles = 1
    for start in chain_start:
        connections = [1]
        current = start
        hub = (hubs & set(modules[start].outputs)).pop()

        while True:
            # Traverse the chains of modules from the start
            for mod in modules[current].outputs:
                # to each node that is _not_ the  hub (or BROADCASTER or start)
                if mod != hub and mod != BROADCASTER and mod != start:
                    current = mod
                    # and store if it outputs to the hub
                    connections.append(int(hub in modules[current].outputs))
                    break
            else:
                break

        # This structure is a binary counter that outputs at a specific number
        # This number is encoded in what nodes in the chain connect to the hub
        period = 0
        for i, n in enumerate(connections):
            period += n*2**i

        # The numbers all happen to be prime
        # so we can multiply them for LCM
        cycles *= period

    return cycles

data = get_data(year=2023, day=20, block=True)

print(part_one(data))
print(part_two_no_eval(data))

assert part_two(data) == part_two_no_eval(data)
