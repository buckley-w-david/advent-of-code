#!/usr/bin/env python

from itertools import permutations
from aocd import get_data
import enum
import queue
import threading

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

class IntCodeInterpreter(threading.Thread):
    def __init__(self, program, iq, oq):
        super().__init__()

        self.memory = program
        self.instruction_pointer = 0
        self.input = iq
        self.output = oq

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

    def exit(self):
        self.executing = False

    def inp(self, dst):
        self.memory[dst] = self.input.get()

    def out(self, value):
        self.output.put(value)

    def run(self):
        self.executing = True
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
    def parse(s, iq, oq):
        return IntCodeInterpreter(literal_eval("[" + s + "]"), iq, oq)


data = get_data(year=2019, day=7, block=True)
outputs = []
for ap, bp, cp, dp, ep in permutations(range(5, 10)):
    aiq = queue.Queue()
    aiq.put(ap)
    aiq.put(0)
    biq = queue.Queue()
    biq.put(bp)
    ciq = queue.Queue()
    ciq.put(cp)
    diq = queue.Queue()
    diq.put(dp)
    eiq = queue.Queue()
    eiq.put(ep)

    a = IntCodeInterpreter.parse(data, aiq, biq)
    b = IntCodeInterpreter.parse(data, biq, ciq)
    c = IntCodeInterpreter.parse(data, ciq, diq)
    d = IntCodeInterpreter.parse(data, diq, eiq)
    e = IntCodeInterpreter.parse(data, eiq, aiq)

    a.start()
    b.start()
    c.start()
    d.start()
    e.start()

    for t in [a,b,c,d,e]:
        t.join()

    outputs.append(aiq.get())
print(max(outputs))
