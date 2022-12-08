#!/usr/bin/env python

print("\033[2J\033[H") # ]]

from aocd import get_data, submit
import re

data = get_data(year=2019, day=2, block=True)
# data = """
# 1,9,10,3,2,3,11,0,99,30,40,50
# """.strip()

class IntCodeInterpreter:
    def __init__(self, program):
        self.memory = program
        self.instruction_pointer = 0

    def execute(self):
        while True:
            opcode = self.memory[self.instruction_pointer]
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
                raise Exception("I am dumbdumb")

    @staticmethod
    def parse(s):
        return IntCodeInterpreter(list(map(int, re.findall("\d+", s))))

for noun in range(100):
    for verb in range(100):
        interpreter = IntCodeInterpreter.parse(data)
        interpreter.memory[1] = noun
        interpreter.memory[2] = verb
        interpreter.execute()
        if interpreter.memory[0] == 19690720:
            print(100 * noun + verb)
            exit()
