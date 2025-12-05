from aoc_utils import *  # type: ignore
from aocd import get_data

data = get_data(year=2024, day=15, block=True)


def to_direction(c):
    if c == "^":
        return Direction.NORTH
    elif c == ">":
        return Direction.EAST
    elif c == "v":
        return Direction.SOUTH
    elif c == "<":
        return Direction.WEST
    assert False


def gps_sum(grid, char="O"):
    s = 0
    for (y, x), c in grid.row_major_with_index():
        if c == char:
            s += 100 * y + x
    return s


def parse(data):
    map, instructions = data.split("\n\n")
    instructions = [to_direction(c) for line in instructions.splitlines() for c in line]
    grid = Grid.parse(map)
    robot = None
    for yx, c in grid.row_major_with_index():
        if c == "@":
            grid[yx] = "."
            robot = yx
            break
    assert robot
    return grid, instructions, robot


def part_one(data):
    grid, instructions, robot = parse(data)

    for direction in instructions:
        dy, dx = direction.value
        ry, rx = robot
        next_position = (ry + dy, rx + dx)
        for yx, c in grid.ray_from_with_index(robot, direction):
            if c == ".":
                grid[yx] = grid[next_position]
                grid[next_position] = "."
                robot = next_position
                break
            elif c == "#":
                break

    return gps_sum(grid)


def part_two(data):
    d = data.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")

    grid, instructions, robot = parse(d)

    for direction in instructions:
        dy, dx = direction.value
        ry, rx = robot
        next_position = (ry + dy, rx + dx)

        if grid[next_position] == ".":
            robot = next_position
        elif grid[next_position] == "#":
            continue
        elif direction is Direction.WEST or direction is direction.EAST:
            target = None
            for yx, c in grid.ray_from_with_index(robot, direction):
                if c == ".":
                    target = yx
                    break
                elif c == "#":
                    break
            else:
                # The board is surrounded by #
                # This should be impossible
                assert False

            if not target:
                continue

            rd = direction.reverse()
            rdy, rdx = rd.value

            grid[target] = grid[(target[0] + rdy, target[1] + rdx)]
            for yx, c in grid.ray_from_with_index(target, direction.reverse()):
                if yx == robot:
                    break

                ny, nx = yx
                grid[yx] = grid[(ny + rdy, nx + rdx)]
            robot = next_position
        else:
            front = {next_position: robot}
            next_front = {}
            if grid[next_position] == "[":
                front[(next_position[0], next_position[1] + 1)] = robot
            elif grid[next_position] == "]":
                front[(next_position[0], next_position[1] - 1)] = robot

            layers = [front]

            blocked = False
            while True:
                clear = True
                for yx in front.keys():
                    if grid[yx] == ".":
                        continue

                    y, x = yx
                    np = (y + dy, x + dx)
                    next_front[np] = yx

                    if grid[np] != ".":
                        clear = False

                    if grid[np] == "#":
                        blocked = True
                        break
                    elif grid[np] == "[":
                        if (y, x + 1) in front.keys():
                            next_front[(y + dy, x + 1)] = (y, x + 1)
                        else:
                            next_front[(y + dy, x + 1)] = robot
                    elif grid[np] == "]":
                        if (y, x - 1) in front.keys():
                            next_front[(y + dy, x - 1)] = (y, x - 1)
                        else:
                            next_front[(y + dy, x - 1)] = robot
                    else:
                        pass
                front = next_front
                next_front = {}
                layers.append(front)
                if clear or blocked:
                    break

            if blocked:
                continue

            for layer in reversed(layers):
                for a, b in layer.items():
                    grid[a] = grid[b]
            robot = next_position

    return gps_sum(grid, char="[")


print(part_one(data))
print(part_two(data))
