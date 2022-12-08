class Tile:
    def __init__(self, id, points, shape):
        self.id = id
        self.points = frozenset(points)
        self.shape = shape

    @staticmethod
    def from_grid(id, tile):
        shape = (len(tile), len(tile))
        points = set()
        for y, row in enumerate(tile):
            for x, col in enumerate(row):
                if col:
                    points.add((y, x))
        return Tile(id, points, shape)

    @staticmethod
    def parse(s):
        lines = s.splitlines()
        m = re.match(r"Tile (\d+):", lines[0])
        id_num = int(m.group(1))
        arr = []
        for y, row in enumerate(lines[1:]):
            r = []
            for x, col in enumerate(row):
                r.append(True if col == '#' else False)
            arr.append(r)
        return Tile.from_grid(id_num, arr)

    def rotated(self):
        n, _ = self.shape
        n -= 1
        s = set()
        for y, x in self.points:
            s.add((x, n-y))
        return Tile(self.id, s, self.shape)

    def flipped(self):
        n, _ = self.shape
        n -= 1
        s = set()
        for y, x in self.points:
            s.add((n-y, x))
        return Tile(self.id, s, self.shape)

    def permutations(self):
        ts = self
        yield self
        for _ in range(3):
            ts = ts.rotated()
            yield ts

        ts = ts.flipped()
        yield ts
        for _ in range(3):
            ts = ts.rotated()
            yield ts

    def edges(self):
        width, height = self.shape
        n = width - 1
        edges = [(0, x) in self.points for x in range(width)]
        yield 0, edges
        yield 0, edges[::-1]
        edges = [(y, n) in self.points for y in range(height)]
        yield 1, edges
        yield 1, edges[::-1]
        edges = [(n, x) in self.points for x in range(width)]
        yield 2, edges
        yield 2, edges[::-1]
        edges = [(y, 0) in self.points for y in range(height)]
        yield 3, edges
        yield 3, edges[::-1]

    def edge(self, edge_id):
        width, height = self.shape
        n = width - 1
        if edge_id == 0:
            return [(0, x) in self.points for x in range(width)]
        elif edge_id == 1:
            return [(y, n) in self.points for y in range(height)]
        elif edge_id == 2:
            return [(n, x) in self.points for x in range(width)]
        elif edge_id == 3:
            return [(y, 0) in self.points for y in range(height)]
        
    FLIP_EDGES = {
        0: 2,
        1: 1,
        2: 0,
        3: 3,
    }

    ROTATE_EDGES = {
        0: 1,
        1: 2,
        2: 3,
        3: 0,
    }

    @staticmethod
    def find_adjacent_edge_transformation(source, target):
        transforms = []
        sl = list(source)
        tl = list(target)

        if Tile.ROTATE_EDGES[source[0]] != source[1]:
            sl[0] = Tile.FLIP_EDGES[sl[0]]
            sl[1] = Tile.FLIP_EDGES[sl[1]]
            transforms.append(Tile.flipped)

        while sl != tl:
            transforms.append(Tile.rotated)
            sl[0] = Tile.ROTATE_EDGES[sl[0]]
            sl[1] = Tile.ROTATE_EDGES[sl[1]]

        return transforms


    def __eq__(self, other):
        return self.id == other.id and self.points == other.points and self.shape == other.shape

    def __hash__(self):
        return hash(self.id) ^ hash(self.points) ^ hash(self.shape)

    def __str__(self):
        h, w = self.shape
        b = [f"Tile {self.id}:\n"] 
        for y in range(h):
            for x in range(w):
                b.append('#' if (y, x) in self.points else '.')
            b.append('\n')
        return ''.join(b)
