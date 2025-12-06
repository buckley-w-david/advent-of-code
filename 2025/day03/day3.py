with open("input.txt") as f:
    data = f.read()


def parse(data):
    return [[int(c) for c in line] for line in data.splitlines()]


def part_one(data):
    s = 0
    for nums in parse(data):
        fc = None
        fi = 0
        for i in range(len(nums) - 1):
            c = nums[i]
            if fc is None or c > fc:
                fc = c
                fi = i
        assert fc

        sc = None
        for i in range(fi + 1, len(nums)):
            c = nums[i]
            if sc is None or c > sc:
                sc = c
        assert sc
        s += 10 * fc + sc

    return s


def part_two(data):
    s = 0
    for nums in parse(data):
        num = 0
        front = 0
        for digit in range(1, 13):
            mc = None
            room = 12 - digit
            for i in range(front, len(nums) - room):
                c = nums[i]
                if mc is None or c > mc:
                    mc = c
                    front = i + 1
            assert mc
            num += mc * 10**room
        s += num

    return s


print(part_one(data))
print(part_two(data))
