from aoc_utils import * # type: ignore
from aocd import get_data

data = get_data(year=2023, day=13, block=True)

def parse_mirrors(chunk):
    rows = [list(l) for l in chunk.splitlines()]
    columns = [['.']*len(rows) for _ in range(len(rows[0]))]
    for x in range(len(rows[0])):
        for y in range(len(rows)):
            columns[x][y] = rows[y][x]
    return rows, columns

def find_reflections(mirrors):
    for line in range(len(mirrors)-1):
        left_min = max(2*line+2 - len(mirrors), 0)
        left_max = line+1

        right_min = line+1
        right_max = line+1+(left_max-left_min)

        before_line = mirrors[left_min:left_max]
        after_line = mirrors[right_min:right_max]

        if before_line == after_line[::-1]:
            yield left_max

def part_one(data):
    chunks = data.split("\n\n")

    t = 0
    for chunk in chunks:
        rows, columns = parse_mirrors(chunk)
        if line := next(find_reflections(columns), None):
            t += line
        elif line := next(find_reflections(rows), None):
            t += 100*line
        else:
            assert False
    return t

def smudged_reflection(chunk):
    rows, columns = parse_mirrors(chunk)
    original_col_reflection = next(find_reflections(columns), None)
    original_row_reflection = next(find_reflections(rows), None)

    for y in range(len(rows)):
        for x in range(len(columns)):
            old = rows[y][x]
            rows[y][x] = columns[x][y] = '.' if old == '#' else '#'

            if reflection := next((l for l in find_reflections(columns) if l != original_col_reflection), None):
                return reflection

            if reflection := next((l for l in find_reflections(rows) if l != original_row_reflection), None):
                return 100*reflection

            rows[y][x] = columns[x][y] = old

    assert False

def part_two(data):
    chunks = data.split("\n\n")

    t = 0
    for chunk in chunks:
        t += smudged_reflection(chunk)

    return t

print(part_one(data))
print(part_two(data))
