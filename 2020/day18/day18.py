#!/usr/bin/env python

from collections import deque
from aocd import get_data, submit

print("\033[2J\033[H") # ]]

data = get_data(year=2020, day=18, block=True)
# data = """
# 1 + (2 * 3) + (4 * (5 + 6))
# 2 * 3 + (4 * 5)
# 5 + (8 * 3 + 9 + 3 * 4 * 3)
# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
# """.strip()

presidence = {
    '*': 1,
    '+': 2,
    '(': 3,
    ')': 3,
}

def eval(a, b, op):
    if op == '+':
        return a + b
    elif op == '*':
        return a * b
    raise Exception()

def eval_expression(expression):
    output_queue = deque()
    op_stack = []
    for token in expression:
        if token.isnumeric():
            output_queue.append(int(token))
        elif token in ['+', '*']:
            while op_stack and op_stack[-1] != '(' and presidence[op_stack[-1]] > presidence[token]:
                output_queue.append(op_stack.pop())
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack[-1] != '(':
                output_queue.append(op_stack.pop())
            assert op_stack[-1] == '('
            op_stack.pop()
    while op_stack:
        assert op_stack[-1] != '('
        output_queue.append(op_stack.pop())

    stack = []
    while output_queue:
        t = output_queue.popleft()
        if not isinstance(t, int):
            a = stack.pop()
            b = stack.pop()
            stack.append(eval(a, b, t))
        else:
            stack.append(t)
    return stack[0]


s = 0
for expression in data.splitlines():
    print(expression, '=', end=' ')
    answer = eval_expression(expression.replace(' ', ''))
    s += answer
    print(answer)
print(s)
