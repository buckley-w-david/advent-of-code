#!/usr/bin/env python

from aocd import get_data
import re

data = get_data(year=2019, day=2, block=True)

tick = 0
class IntCodeInterpreter:
    def __init__(self, program):
        self.memory = program
        self.instruction_pointer = 0

    def execute(self):
        global tick
        while True:
            # if self.memory[1] == 4 and self.memory[2] == 1:
            #     breakpoint()
            opcode = self.memory[self.instruction_pointer]
            tick += 1
            if opcode == 1:
                i1, i2, o = self.memory[self.instruction_pointer+1:self.instruction_pointer+4]
                self.memory[o] = self.memory[i1] + self.memory[i2]
                self.instruction_pointer += 4
            elif opcode == 2:
                i1, i2, o = self.memory[self.instruction_pointer+1:self.instruction_pointer+4]
                self.memory[o] = self.memory[i1] * self.memory[i2]
                self.instruction_pointer += 4
            elif opcode == 99:
                return
            else:
                raise Exception("Bad")

    @staticmethod
    def parse(s):
        return IntCodeInterpreter(list(map(int, re.findall(r"\d+", s))))

for noun in range(100):
    for verb in range(100):
        print(noun, verb)
        interpreter = IntCodeInterpreter.parse(data)
        interpreter.memory[1] = noun
        interpreter.memory[2] = verb
        interpreter.execute()
        if interpreter.memory[0] == 19690720:
            print(100 * noun + verb)
            exit()
