class IntersectionError(Exception):
    pass

class Range:
    def __init__(self, start: int, stop: int, step: int = 1):
        self._r = range(start, stop, step)

    @property
    def start(self) -> int:
        return self._r.start

    @property
    def stop(self) -> int:
        return self._r.stop

    @property
    def step(self) -> int:
        return self._r.step

    def __iter__(self):
        return iter(self._r)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f'Range({self.start}, {self.stop}, {self.step})'

    def includes(self, r: 'Range') -> bool:
        return self.start <= r.start and self.stop >= r.stop

    def inside(self, r: 'Range') -> bool:
        return self.start >= r.start and self.stop <= r.stop
    
    def contains(self, r: 'Range') -> bool:
        return self.inside(r)

    def intersects(self, r: 'Range') -> bool:
        return r.start <= self.start <= r.stop or self.start <= r.start <= self.stop

    def disjoint(self, r: 'Range') -> bool:
        return not self.intersects(r)

    def askew(self, r: 'Range') -> bool:
        return self.disjoint(r)

    def intersection(self, r: 'Range') -> 'Range':
        if not self.intersects(r):
            raise IntersectionError(f"{self} and {r} do not intersect")
        return Range(max(self.start, r.start), min(self.stop, r.stop))

    def overlap(self, r: 'Range') -> 'Range':
        return self.intersection(r)

    def __and__(self, r: 'Range') -> 'Range':
        return self.intersection(r)

    def union(self, r: 'Range') -> 'Range':
        if not self.intersects(r):
            raise IntersectionError(f"{self} and {r} do not intersect")
        return Range(min(self.start, r.start), max(self.stop, r.stop))

    def __or__(self, r: 'Range') -> 'Range':
        return self.union(r)
