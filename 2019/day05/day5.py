#!/usr/bin/env python

from aocd import get_data
import re
import itertools

data = get_data(year=2019, day=5, block=True)

class IntCodeInterpreter:
    def __init__(self, program):
        self.memory = program
        self.instruction_pointer = 0

    def retrieve_parameter(self, p):
        mode, parameter = p
        if mode == 0:
            return self.memory[parameter]
        elif mode == 1:
            return parameter
        else:
            raise ValueError("blah")

    def execute(self):
        while True:
            opcode = self.memory[self.instruction_pointer]
            mode_mask = opcode // 100
            opcode = opcode % 100
            modes = []
            while mode_mask > 0:
                modes.append(mode_mask % 10)
                mode_mask //= 10
            modes = itertools.chain(modes, itertools.repeat(0))
            if opcode == 1:
                i1, i2 = map(self.retrieve_parameter, zip(modes, self.memory[self.instruction_pointer+1:self.instruction_pointer+3]))
                o = self.memory[self.instruction_pointer+3]
                self.memory[o] = i1 + i2
                self.instruction_pointer += 4
            elif opcode == 2:
                i1, i2 = map(self.retrieve_parameter, zip(modes, self.memory[self.instruction_pointer+1:self.instruction_pointer+3]))
                o = self.memory[self.instruction_pointer+3]
                self.memory[o] = i1 * i2 
                self.instruction_pointer += 4
            elif opcode == 3:
                o = self.memory[self.instruction_pointer+1]
                self.memory[o] = int(input("input: "))
                self.instruction_pointer += 2
            elif opcode == 4:
                param = map(self.retrieve_parameter, zip(modes, [self.memory[self.instruction_pointer+1]]))
                print(next(param))
                self.instruction_pointer += 2
            elif opcode == 99:
                return
            else:
                raise Exception("I am dumbdumb: %s" % opcode)

    @staticmethod
    def parse(s):
        return IntCodeInterpreter(list(map(int, re.findall("\d+", s))))

interpreter = IntCodeInterpreter.parse(data)
interpreter.execute()
