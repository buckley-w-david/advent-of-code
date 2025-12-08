from typing import Generic, TypeVar

T = TypeVar("T")


class UnionFind(Generic[T]):
    def __init__(self, elements: list[T]):
        self.parents = dict()
        self.size = dict()
        for element in elements:
            self.parents[element] = element
            self.size[element] = 1

    def find(self, value: T) -> T:
        if value == self.parents[value]:
            return value

        self.parents[value] = self.find(self.parents[value])

        return self.parents[value]

    def union(self, a: T, b: T):
        a = self.find(a)
        b = self.find(b)

        if a != b:
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.parents[b] = a
            self.size[a] += self.size[b]

    def add(self, value: T):
        self.parents[value] = value
        self.size[value] = 1
