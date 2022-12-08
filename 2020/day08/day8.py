#!/usr/bin/env python

from aocd import get_data, submit

data = get_data(year=2020, day=8, block=True)
# data = """
# nop +0
# acc +1
# jmp +4
# acc +3
# jmp -3
# acc -99
# acc +1
# jmp -4
# acc +6
# """.strip()

class InfiniteLoopError(Exception):
    pass

class Console:
    def __init__(self, instructions):
        self.acc = 0
        self.p_counter = 0
        self.instructions = instructions
        self.stop = len(self.instructions)

    @staticmethod
    def from_source(source):
        instructions = []
        for line in source.strip().split("\n"):
            instruction, arg = line.split()
            instructions.append((instruction, int(arg)))

        return Console(instructions)

    def on_acc(self, arg):
        self.acc += arg
        self.p_counter += 1

    def on_jmp(self, arg):
        self.p_counter += arg

    def on_nop(self, _arg):
        self.p_counter += 1

    def step(self):
        instruction, argument = self.instructions[self.p_counter]
        if instruction == "acc":
            self.on_acc(argument)
        elif instruction == "jmp":
            self.on_jmp(argument)
        elif instruction == "nop":
            self.on_nop(argument)
        return self.p_counter

    def run_to_termination(self):
        history = set()
        while self.p_counter != self.stop:
            if self.p_counter in history:
                raise InfiniteLoopError(self.p_counter)
            history.add(self.p_counter)
            self.step()
        return self.acc


instructions = Console.from_source(data).instructions
terminates = False
for idx in range(len(instructions)):
    (instr, arg) = instructions[idx]
    if instr == 'jmp':
        instructions[idx] = ('nop', arg)
    elif instr == 'nop':
        instructions[idx] = ('jmp', arg)
    else:
        continue
    console = Console(instructions)
    try:
        acc = console.run_to_termination()
        print(acc)
        break
    except InfiniteLoopError as e:
        instructions[idx] = (instr, arg)


