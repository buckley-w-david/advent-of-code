from aocd import get_data

data = get_data(year=2025, day=4, block=True)


def parse(data):
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            grid[(y, x)] = char == "@"
    return grid


def adjacent(grid, position):
    y, x = position
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            if dy == 0 and dx == 0:
                continue
            yy = y + dy
            xx = x + dx
            if (yy, xx) not in grid:
                continue
            yield grid[(yy, xx)]


def part_one(data):
    grid = parse(data)
    count = 0
    for position in grid:
        count += grid[position] and sum(adjacent(grid, position)) < 4
    return count


def part_two(data):
    grid = parse(data)
    count = 0
    removed = True
    while removed:
        removed = False
        for position in grid:
            if grid[position] and sum(adjacent(grid, position)) < 4:
                count += 1
                grid[position] = False
                removed = True
    return count


print(part_one(data))
print(part_two(data))
