#!/usr/bin/env python

from aocd import get_data
import re
import enum

from ast import literal_eval

class Mode(enum.IntEnum):
    POSITION = 0
    IMMEDIATE = 1

class Opcode(enum.IntEnum):
    ADD  = 1
    MUL  = 2
    INP  = 3
    OUT  = 4
    JIT  = 5
    JIF  = 6
    LT   = 7
    EQ   = 8
    EXIT = 99

def noop(*args, **kwargs):
    return 0

from typing import Any, Callable
class IntCodeInterpreter:


    def __init__(self, program, input: Callable[[], int] = noop, output: Callable[[int], Any] = noop):
        self.memory = program
        self.instruction_pointer = 0
        self.input = input
        self.output = output

        self.opcodes = {
            # OPCODE     IN ARGS, OUT ARGS
            Opcode.ADD:  (2, 1),
            Opcode.MUL:  (2, 1),
            Opcode.JIT:  (2, 0),
            Opcode.JIF:  (2, 0),
            Opcode.LT:   (2, 1),
            Opcode.EQ:   (2, 1),
            Opcode.INP:  (0, 1),
            Opcode.OUT:  (1, 0),
            Opcode.EXIT: (0, 0),
        }

    def get(self, i, mode):
        if mode == Mode.POSITION:
            return self.memory[i]
        elif mode == Mode.IMMEDIATE:
            return i

    def params(self, n, modes):
        args = []
        for i in range(self.instruction_pointer+1, self.instruction_pointer+n+1):
            mode = modes % 10
            modes //= 10
            args.append(self.get(self.memory[i], mode))
        self.instruction_pointer += n
        return args

    def add(self, a, b, out):
        self.memory[out] = a + b

    def mul(self, a, b, out):
        self.memory[out] = a * b

    def jit(self, p, dst):
        if p != 0:
            self.instruction_pointer = dst - 1 # minus 1 to account for automatic increment in execute 

    def jif(self, p, dst):
        if p == 0:
            self.instruction_pointer = dst - 1 # minus 1 to account for automatic increment in execute 

    def lt(self, a, b, out):
        if a < b:
            self.memory[out] = 1
        else:
            self.memory[out] = 0

    def eq(self, a, b, out):
        if a == b:
            self.memory[out] = 1
        else:
            self.memory[out] = 0

    def inp(self, dst):
        self.memory[dst] = self.input()

    def out(self, value):
        self.output(value)

    def exit(self):
        self.executing = False

    def execute(self):
        self.executing = True
        # breakpoint()
        while self.executing:
            raw_code = self.memory[self.instruction_pointer]
            opcode = Opcode(raw_code % 100)
            param_modes = raw_code // 100
            inargs, onargs = self.opcodes[opcode]

            in_ = self.params(inargs, param_modes)

            # TODO: Might need to improve output arg fetching later
            out = self.memory[self.instruction_pointer+1:self.instruction_pointer+onargs+1]
            self.instruction_pointer += onargs

            getattr(self, f'{opcode.name.lower()}')(*in_, *out)
            self.instruction_pointer += 1

    @staticmethod
    def parse(s, input: Callable[[], int] = noop, output: Callable[[int], Any] = noop):
        return IntCodeInterpreter(literal_eval("[" + s + "]"), input, output)

def program_input():
    return 5

data = get_data(year=2019, day=5, block=True)
computer = IntCodeInterpreter.parse(data, program_input, print)
computer.execute()
