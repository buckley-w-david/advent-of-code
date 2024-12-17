from math import log
from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=17, block=True)


class VirtualMachine:
    def __init__(self, program, a, b, c) -> None:
        self.program = program
        self.a = a
        self.b = b
        self.c = c
        self.instruction_pointer = 0
        self.vtable = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdb,
        }
        self.output = []

    def combo(self, op: int):
        if 0 <= op <= 3:
            return op
        elif op == 4:
            return self.a
        elif op == 5:
            return self.b
        elif op == 6:
            return self.c
        else:
            assert False

    def adv(self, op):
        self.a = int(self.a / 2 ** self.combo(op))
        return 2

    def bxl(self, op):
        self.b = self.b ^ op
        return 2

    def bst(self, op):
        self.b = self.combo(op) % 8
        return 2

    def jnz(self, op):
        if self.a == 0:
            return 2
        self.instruction_pointer = op
        return 0

    def bxc(self, _):
        self.b = self.b ^ self.c
        return 2

    def out(self, op):
        self.output.append(self.combo(op) % 8)
        return 2

    def bdv(self, op):
        self.b = int(self.a / 2 ** self.combo(op))
        return 2

    def cdb(self, op):
        self.c = int(self.a / 2 ** self.combo(op))
        return 2

    def run(self):
        self.output = []
        self.instruction_pointer = 0
        while self.instruction_pointer >= 0 and self.instruction_pointer < len(
            self.program
        ):
            op, arg = self.program[
                self.instruction_pointer : self.instruction_pointer + 2
            ]
            func = self.vtable[op]
            pci = func(arg)
            self.instruction_pointer += pci

        return self.output

    @classmethod
    def parse(cls, source):
        reg, prg = source.split("\n\n")
        a, b, c = ints(reg)
        program = ints(prg)

        return cls(program, a, b, c)


def part_one(data):
    vm = VirtualMachine.parse(data)
    return ",".join(map(str, vm.run()))


def part_two(data):
    vm = VirtualMachine.parse(data)
    target = vm.program
    program_num = int("".join(map(str, vm.program)), base=8)
    digits = int(log(program_num, 8))

    guess = 8**digits
    r = digits
    while r >= 0:
        for i in range(8):
            ng = guess + (i * 8**r)
            vm.a = ng
            out = vm.run()
            if out[r] == target[r]:
                guess = ng
                break
        else:
            guess = guess + (1 * 8 ** (r - 1))
            continue
        r -= 1

    vm.a = guess
    # registers b and c turn out to be irrelevant, they'll just overwritten by data based on a
    assert vm.run() == target

    return guess


print(part_one(data))
print(part_two(data))
