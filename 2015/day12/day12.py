import json
from aoc_utils import *
from aocd import get_data

data = get_data(year=2015, day=12, block=True)

document = json.loads(data)


def traverse_document(doc, func):
    if isinstance(doc, list):
        for item in doc:
            traverse_document(item, func)
    elif isinstance(doc, dict):
        for item in doc.values():
            traverse_document(item, func)
    else:
        func(doc)


def traverse_document_skip_red(doc, func):
    if isinstance(doc, list):
        for item in doc:
            traverse_document_skip_red(item, func)
    elif isinstance(doc, dict):
        for item in doc.values():
            if item == "red":
                return

        for item in doc.values():
            traverse_document_skip_red(item, func)
    else:
        func(doc)


def part_one(data):
    document = json.loads(data)
    s = 0

    def add(item):
        if isinstance(item, int):
            nonlocal s
            s += item

    traverse_document(document, add)
    return s


def part_two(data):
    document = json.loads(data)
    s = 0

    def add(item):
        if isinstance(item, int):
            nonlocal s
            s += item

    traverse_document_skip_red(document, add)
    return s


print(part_one(data))
print(part_two(data))
