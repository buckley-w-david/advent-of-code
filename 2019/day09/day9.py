#!/usr/bin/env python

from aocd import get_data
import enum
import queue
import threading

from ast import literal_eval

class Mode(enum.IntEnum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

class Opcode(enum.IntEnum):
    ADD  = 1
    MUL  = 2
    INP  = 3
    OUT  = 4
    JIT  = 5
    JIF  = 6
    LT   = 7
    EQ   = 8
    ADJ  = 9
    EXIT = 99

class IntCodeInterpreter(threading.Thread):
    def __init__(self, program, iq, oq):
        super().__init__()

        self.memory = program
        self.instruction_pointer = 0
        self.input = iq
        self.output = oq
        self.relative_base = 0

        self.opcodes = {
            # OPCODE     IN ARGS, OUT ARGS
            Opcode.ADD:  (2, 1),
            Opcode.MUL:  (2, 1),
            Opcode.JIT:  (2, 0),
            Opcode.JIF:  (2, 0),
            Opcode.LT:   (2, 1),
            Opcode.EQ:   (2, 1),
            Opcode.ADJ:  (1, 0),
            Opcode.INP:  (0, 1),
            Opcode.OUT:  (1, 0),
            Opcode.EXIT: (0, 0),
        }

    def realloc(self, addr):
        # This is a bit of a hack
        # Whenever we hit an address that is off the end of existing memory we extend memory by the difference with 0s
        assert addr >= 0
        max_addr = len(self.memory)-1
        diff = addr-max_addr
        if diff > 0:
            self.memory.extend([0]*diff)

    def setmem(self, addr, value):
        self.realloc(addr)
        self.memory[addr] = value

    def getmem(self, addr):
        self.realloc(addr)
        return self.memory[addr]

    def get_param(self, i, mode, out):
        if mode == Mode.POSITION:
            return i if out else self.getmem(i)
        elif mode == Mode.IMMEDIATE:
            return i
        elif mode == Mode.RELATIVE:
            target = self.relative_base+i 
            return target if out else self.getmem(target)

    def params(self, n, modes, out=False):
        args = []
        for i in range(self.instruction_pointer+1, self.instruction_pointer+n+1):
            mode = modes % 10
            modes //= 10
            args.append(self.get_param(self.getmem(i), mode, out))
        self.instruction_pointer += n
        return args

    def add(self, a, b, out):
        self.setmem(out, a+b)

    def mul(self, a, b, out):
        self.setmem(out, a*b)

    def jit(self, p, dst):
        if p != 0:
            self.instruction_pointer = dst - 1 # minus 1 to account for automatic increment in run 

    def jif(self, p, dst):
        if p == 0:
            self.instruction_pointer = dst - 1 # minus 1 to account for automatic increment in run 

    def lt(self, a, b, out):
        self.setmem(out, int(a < b))

    def eq(self, a, b, out):
        self.setmem(out, int(a == b))

    def adj(self, amt):
        self.relative_base += amt

    def exit(self):
        self.executing = False

    def inp(self, dst):
        self.setmem(dst, self.input.get())

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
            if in_:
                param_modes //= 10**len(in_)
            out = self.params(onargs, param_modes, out=True)

            getattr(self, f'{opcode.name.lower()}')(*in_, *out)
            self.instruction_pointer += 1

    @staticmethod
    def parse(s, iq, oq):
        return IntCodeInterpreter(literal_eval("[" + s + "]"), iq, oq)


iq = queue.Queue()
oq = queue.Queue()
iq.put(2)

data = get_data(year=2019, day=9, block=True)
interpreter = IntCodeInterpreter.parse(data, iq, oq)
interpreter.run()
print([oq.get() for _ in range(oq.qsize())])
