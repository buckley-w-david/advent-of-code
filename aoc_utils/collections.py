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
    return chunk(l, len(l)//n)
