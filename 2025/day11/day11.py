from collections import defaultdict
from functools import cache
from aocd import get_data

data = get_data(year=2025, day=11, block=True)


def parse(data):
    graph = defaultdict(set)
    for line in data.splitlines():
        left, right = line.split(": ")
        for node in right.split(" "):
            graph[left].add(node)

    return graph


def part_one(data):
    graph = parse(data)

    @cache
    def count_paths(node):
        if node == "out":
            return 1
        return sum(count_paths(n) for n in graph[node])

    return count_paths("you")


# I thought of both of these solutions almost right away
# not sure which I like better, so I just included both ¯\_(ツ)_/¯
def part_two(data):
    graph = parse(data)

    @cache
    def count_paths(node, dac, fft):
        if node == "out":
            return dac and fft

        return sum(
            count_paths(n, dac or node == "dac", fft or node == "fft")
            for n in graph[node]
        )

    return count_paths("svr", False, False)


def part_two_again(data):
    graph = parse(data)

    @cache
    def count_paths(node, target):
        if node == target:
            return 1

        return sum(count_paths(n, target) for n in graph[node])

    # This is a DAG
    # either fft comes first on the way to out, or dac does
    # that means one of these will be 0, the other will be part of our solution
    fft_to_dac = count_paths("fft", "dac")
    dac_to_fft = count_paths("dac", "fft")
    assert fft_to_dac == 0 or dac_to_fft == 0

    first, second = "fft", "dac"
    middle = fft_to_dac
    if fft_to_dac == 0:
        first, second = "dac", "fft"
        middle = dac_to_fft

    return count_paths("svr", first) * middle * count_paths(second, "out")


print(part_one(data))
print(part_two(data))
print(part_two_again(data))
