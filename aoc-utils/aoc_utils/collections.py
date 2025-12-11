import itertools


def maxn(l, n):
    return sorted(l)[-n:]


def minn(l, n):
    return sorted(l)[:n]


def take(l, n):
    return list(itertools.islice(iter(l), 0, n))


def chunk(l, n):
    li = iter(l)
    while True:
        group = take(li, n)
        if group:
            yield group
        else:
            break


def groups(l, n):
    return chunk(l, len(l) // n)


def alternating(*iterables):
    for values in zip(*iterables):
        for value in values:
            yield value


def transpose(l):
    return list(zip(*l))


def powerset(iterable):
    "Subsequences of the iterable from shortest to longest."
    # powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )
