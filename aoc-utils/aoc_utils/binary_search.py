from abc import abstractmethod
from typing import TypeVar, Callable, Protocol

class Ordered(Protocol):
    @abstractmethod
    def __lt__(self: 'T', other: 'T', /) -> bool:
        ...

    @abstractmethod
    def __eq__(self: 'T', other: 'T', /) -> bool:
        ...

T = TypeVar('T', bound=Ordered)

def binary_search(left_bound: int, right_bound: int, getter: Callable[[int], T], element: T):
    while left_bound <= right_bound:
        mid = (left_bound+right_bound) // 2
        e = getter(mid)
        if e == element:
            return mid
        elif e < element:
            left_bound = mid + 1
        else:
            right_bound = mid - 1
    return None
