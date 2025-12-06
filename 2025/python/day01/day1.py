import math

with open("input.txt", "r") as f:
    data = f.read()


def part_one(data):
    lines = data.splitlines()
    n = 50
    password = 0
    for line in lines:
        d, steps = line[0], int(line[1:])
        direction = -1 if d == "L" else 1
        n = (n + direction * steps) % 100
        if n == 0:
            password += 1

    return password


def part_two(data):
    lines = data.splitlines()
    n = 50
    password = 0
    for line in lines:
        d, steps = line[0], int(line[1:])
        direction = -1 if d == "L" else 1

        nn = n + direction * steps

        if nn <= 0:
            password += (n != 0) - math.trunc(nn / 100)
        elif nn >= 100:
            password += nn // 100

        n = nn % 100

    return password


print(part_one(data))
print(part_two(data))
