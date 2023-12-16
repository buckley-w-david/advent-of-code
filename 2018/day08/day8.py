from aoc_utils import *
from aocd import get_data

data = get_data(year=2018, day=8, block=True)

class Node:
    def __init__(self, children: list['Node'], metadata: list[int]):
        self.children = children
        self.metadata = metadata

    def depth_first_traversal(self, visit):
        visit(self)
        for child in self.children:
            child.depth_first_traversal(visit)

    def value(self):
        if not self.children:
            return sum(self.metadata)
        else:
            return sum(self.children[m-1].value() for m in self.metadata if (m-1) < len(self.children))

def parse_node(numbers: list[int], cursor=0):
    n_children, n_metadata, *_ = numbers[cursor:]
    children = []
    cursor += 2
    for _ in range(n_children):
        node, cursor = parse_node(numbers, cursor)
        children.append(node)
    metadata = numbers[cursor:cursor+n_metadata]
    node = Node(children, metadata)
    return (node, cursor+n_metadata)

def part_one(data):
    numbers = ints(data)
    (tree, _) = parse_node(numbers)
    s = 0
    def total(node):
        nonlocal s
        for m in node.metadata:
            s += m

    tree.depth_first_traversal(total)
    return s

def part_two(data):
    numbers = ints(data)
    (tree, _) = parse_node(numbers)
    return tree.value()

print(part_one(data))
print(part_two(data))

