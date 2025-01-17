from collections import deque
from aoc_utils import *  # type: ignore

from aocd import get_data

data = get_data(year=2024, day=9, block=True)


def checksum_contiguous_disk(disk):
    checksum = 0
    for i, file_id in enumerate(disk):
        if file_id is None:
            return checksum
        checksum += i * file_id
    return checksum


def parse_one(data):
    blocks = [int(c) for c in data]
    disk = [None] * sum(blocks)
    state = True
    head = 0
    file_id = 0
    holes = deque([])
    files = {}
    for block in blocks:
        if state:
            disk[head : head + block] = [file_id] * block
            files[file_id] = list(range(head + block - 1, head - 1, -1))
            state = False
            file_id += 1
        else:
            holes.extend(range(head, head + block))
            state = True
        head += block
    return disk, holes, files


def part_one(data):
    disk, holes, files = parse_one(data)
    for file_id in list(reversed(files.keys())):
        positions = files[file_id]
        i = 0
        while holes and i < len(positions):
            if holes[0] > positions[i]:
                return checksum_contiguous_disk(disk)
            h = holes.popleft()
            disk[h] = file_id
            disk[positions[i]] = None
            i += 1
    return checksum_contiguous_disk(disk)


def parse_two(data):
    blocks = [int(c) for c in data]
    disk = [None] * sum(blocks)
    state = True
    head = 0
    file_id = 0
    holes = []
    files = {}
    for block in blocks:
        if state:
            disk[head : head + block] = [file_id] * block
            files[file_id] = (head, head + block)
            file_id += 1
        elif block != 0:
            holes.append((head, head + block))
        state = not state
        head += block
    return disk, holes, files


def checksum(disk):
    checksum = 0
    for i, file_id in enumerate(disk):
        if file_id is None:
            continue
        checksum += i * file_id
    return checksum


def part_two(data):
    disk, holes, files = parse_two(data)
    for file_id in list(reversed(files.keys())):
        start, end = files[file_id]
        length = end - start
        for i, (hs, he) in enumerate(holes):
            hl = he - hs
            if hs > start:
                break
            if length <= hl:
                disk[hs : hs + length] = [file_id] * length
                disk[start:end] = [None] * length
                if length == hl:
                    holes.pop(i)
                else:
                    holes[i] = (hs + length, he)
                before_start = None
                after_end = None
                # FIXME: O(n**2) is bad
                for i, (hs, he) in enumerate(reversed(holes)):
                    j = len(holes) - i - 1
                    if hs == end:
                        after_end = (j, (hs, he))
                    elif he == start:
                        before_start = (j, (hs, he))
                    if he < start:
                        break
                if before_start and after_end:
                    (i, (hs, _)) = before_start
                    (ri, (_, he)) = after_end
                    holes.pop(ri)
                elif before_start:
                    (i, (hs, _)) = before_start
                    he = end
                elif after_end:
                    (i, (_, he)) = after_end
                    hs = start
                else:
                    # This is technically incorrect, but the only time it matters is the very rightmost file
                    # Since we only ever try to move a file once, this doesn't actually come into play
                    break
                holes[i] = (hs, he)
                break

    return checksum(disk)


print(part_one(data))
print(part_two(data))
