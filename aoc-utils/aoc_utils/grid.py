import enum
from typing import List, TypeVar, Tuple, Union, Generic, Iterator, Callable, cast

S = TypeVar("S")
T = TypeVar("T")


class Direction(enum.Enum):
    NORTH = (-1, 0)
    NE = (-1, 1)
    EAST = (0, 1)
    SE = (1, 1)
    SOUTH = (1, 0)
    SW = (1, -1)
    WEST = (0, -1)
    NW = (-1, -1)

    @staticmethod
    def cardinal():
        return [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]

    def __add__(self, coordinates: Tuple[int, int]) -> Tuple[int, int]:
        y, x = coordinates
        dy, dx = self.value
        return (y + dy, x + dx)

    def __radd__(self, coordinates: Tuple[int, int]) -> Tuple[int, int]:
        return self.__add__(coordinates)

    def __sub__(self, coordinates: Tuple[int, int]) -> Tuple[int, int]:
        y, x = coordinates
        dy, dx = self.value
        return (y - dy, x - dx)

    def __rsub__(self, coordinates: Tuple[int, int]) -> Tuple[int, int]:
        return self.__sub__(coordinates)

    def reverse(self):
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.NORTH
        elif self == Direction.EAST:
            return Direction.WEST
        elif self == Direction.WEST:
            return Direction.EAST
        raise

    def rotate(self, handedness: int = 1, cardinal: bool = False):
        mod = 4 if cardinal else 8
        directions = Direction.cardinal() if cardinal else list(Direction)
        index = directions.index(self)
        return directions[(index + handedness) % mod]


class Grid(Generic[T]):
    def __init__(self, arr: List[List[T]]) -> None:
        self.arr = arr

    @staticmethod
    def parse(grid: str, cast: Callable[[str], T] = str) -> "Grid[T]":
        return Grid([[cast(c) for c in line] for line in grid.splitlines()])

    @property
    def height(self) -> int:
        return len(self.arr)

    @property
    def width(self) -> int:
        return len(self.arr[0])

    def __str__(self):
        lines = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                line.append(self.arr[y][x])
            lines.append("".join(line))
        return "\n".join(lines)

    def print(self, highlight=[], colour=31):
        for y in range(self.height):
            for x in range(self.width):
                if (y, x) in highlight:
                    print(f"\033[{colour};1;4m{self.arr[y][x]}\033[0m", end="")
                else:
                    print(self.arr[y][x], end="")
            print()

    def __contains__(self, yx: Tuple[int, int]) -> bool:
        y, x = yx
        return 0 <= y < self.height and 0 <= x < self.width

    def __getitem__(self, yx: Union[Tuple[int, int], int]) -> Union[T, List[T]]:
        if isinstance(yx, tuple):
            if yx not in self:
                raise IndexError
            y, x = yx
            return self.arr[y][x]
        elif not isinstance(yx, int):
            raise TypeError
        return self.arr[yx]

    def __setitem__(self, yx: Tuple[int, int], item: T) -> None:
        y, x = yx
        self.arr[y][x] = item

    def __iter__(self) -> Iterator[T]:
        return self.row_major()

    def get(self, yx: Tuple[int, int], default: T | None = None) -> T | None:
        if yx in self:
            return cast(T, self[yx])
        return default

    def insert_row(self, y: int, row: List[T]):
        self.arr.insert(y, row)

    def insert_column(self, x: int, column: List[T]):
        for value, row in zip(column, self.arr):
            row.insert(x, value)

    def row_major_with_index(self) -> Iterator[Tuple[Tuple[int, int], T]]:
        for i in range(self.height):
            for j in range(self.width):
                yield ((i, j), self.arr[i][j])

    def row_major(self) -> Iterator[T]:
        yield from (item for (_, item) in self.row_major_with_index())

    def column_major_with_index(self) -> Iterator[Tuple[Tuple[int, int], T]]:
        for i in range(self.width):
            for j in range(self.height):
                yield ((i, j), self.arr[j][i])

    def column_major(self) -> Iterator[T]:
        yield from (item for (_, item) in self.column_major_with_index())

    def apply(self, func: Callable[[T], None]) -> None:
        for item in self:
            func(item)

    def map(self, func: Callable[[T], S]) -> "Grid[S]":
        return Grid([[func(item) for item in row] for row in self.arr])

    def ray_from(self, yx: Tuple[int, int], direction: Direction) -> Iterator[T]:
        yield from (item for (_, item) in self.ray_from_with_index(yx, direction))

    def ray_from_with_index(
        self, yx: Tuple[int, int], direction: Direction
    ) -> Iterator[Tuple[Tuple[int, int], T]]:
        if yx not in self:
            raise IndexError

        y, x = yx
        dy, dx = direction.value
        y += dy
        x += dx
        while (y, x) in self:
            yield ((y, x), self.arr[y][x])
            y += dy
            x += dx

    def around_with_index(
        self, yx: Tuple[int, int], corners: bool = True
    ) -> Iterator[Tuple[Tuple[int, int], T]]:
        y, x = yx
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not corners and abs(i) == abs(j):
                    continue
                p = (y + i, x + j)
                if p != yx and p in self:
                    yield (p, self.arr[y + i][x + j])

    def around(self, yx: Tuple[int, int], corners: bool = True) -> Iterator[T]:
        for (_, _), elem in self.around_with_index(yx, corners):
            yield elem
