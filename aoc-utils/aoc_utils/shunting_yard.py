from collections import deque
import re

DEFAULT_PRESIDENCE = {
    '^': 10,
    '*': 20,
    '/': 20,
    '+': 30,
    '-': 30,
}

class ShuntingYard:
    def __init__(self, presidence = None):
        if presidence is None:
            self.presidence = DEFAULT_PRESIDENCE

    def eval(self, left: int, right: int, operator: str):
        if operator not in self.presidence:
            raise ValueError(f"\"{operator}\" not a known token")
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '/':
            return left / right
        elif operator == '*':
            return left * right
        elif operator == '^':
            return left ** right
        raise Exception() # absurd


    def __call__(self, expression, strip_whitespace=True):
        if strip_whitespace:
            expression = re.sub(r"\s+", '', expression)

        presidence = self.presidence
        output_queue = deque()
        op_stack = []
        for token in expression:
            if token.isnumeric():
                output_queue.append(int(token)) # TODO multicharacter numbers
            elif token in presidence:
                while op_stack and op_stack[-1] != '(' and presidence[op_stack[-1]] < presidence[token]:
                    output_queue.append(op_stack.pop())
                op_stack.append(token)
            elif token == '(':
                op_stack.append(token)
            elif token == ')':
                while op_stack[-1] != '(':
                    output_queue.append(op_stack.pop())
                assert op_stack[-1] == '('
                op_stack.pop()
            else:
                raise ValueError(f"\"{token}\" not a known token")
        while op_stack:
            assert op_stack[-1] != '('
            output_queue.append(op_stack.pop())

        stack = []
        while output_queue:
            t = output_queue.popleft()
            if not isinstance(t, int):
                a = stack.pop()
                b = stack.pop()
                stack.append(self.eval(a, b, t))
            else:
                stack.append(t)
        return stack[0]
