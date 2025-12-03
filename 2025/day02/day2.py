import itertools

with open("input.txt", "r") as f:
    data = f.read()


def parse(data):
    return [[int(i) for i in r.split("-")] for r in data.split(",")]


def sum_invalid(ranges, validate):
    sum = 0
    for start, end in ranges:
        for n in range(start, end + 1):
            if not validate(n):
                sum += n

    return sum


def part_one(data):
    def validate(n):
        s = str(n)
        l = len(s)
        return s[: l // 2] != s[l // 2 :]

    return sum_invalid(parse(data), validate)


def part_two(data):
    def validate(n):
        s = str(n)
        length = len(s)
        for segment_size in range(1, length // 2 + 1):
            if length % segment_size != 0:
                continue

            if len(set(itertools.batched(s, segment_size))) == 1:
                return False
        return True

    return sum_invalid(parse(data), validate)


print(part_one(data))
print(part_two(data))
