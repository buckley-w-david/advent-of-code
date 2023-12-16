from abc import abstractmethod
from typing import Callable, Optional, TypeVar, Protocol, Generic, cast

class Ordered(Protocol):
    @abstractmethod
    def __lt__(self: 'T', other: 'T', /) -> bool:
        ...

    @abstractmethod
    def __eq__(self: 'T', other: 'T', /) -> bool:
        ...

import enum
class Colour(enum.Enum):
    RED = enum.auto()
    BLACK = enum.auto()

T = TypeVar('T', bound=Ordered)
class BinaryNode(Generic[T]):
    def __init__(self, value: T, tree: 'BinarySearchTree[T]', parent: Optional['BinaryNode[T]'] = None):
        self.value = value

        self.left = None
        self.right = None
        self.parent = parent
        self.tree = tree

    def insert(self, value: T):
        if value < self.value:
            if self.left is None:
                self.left = type(self)(value, self.tree, self)
                return self.left
            else:
                return self.left.insert(value)
        elif value > self.value:
            if self.right is None:
                self.right = type(self)(value, self.tree, self)
                return self.right
            else:
                return self.right.insert(value)
        # attempt to insert duplicate node
        return self

    def delete(self, value: T):
        node = self.find(value)
        if node is None: return

        if node.left is None:
            node._transplant(node.right)
        elif node.right is None:
            node._transplant(node.left)
        else:
            y = node.right
            while y.left is not None:
                y = y.left

            if y is not node.right:
                y._transplant(y.right)
                y.right = node.right
                cast('BinaryNode[T]', y.right).parent = y

            node._transplant(y)
            y.left = node.left
            cast('BinaryNode[T]', y.left).parent = y

    def _transplant(self, v: Optional['BinaryNode[T]']):
        if self.parent is None:
            self.tree.root_node = v
        elif self.is_left_child():
            self.parent.left = v
        else:
            self.parent.right = v

        if v is not None:
            v.parent = self.parent

    def find(self, value: T):
        if value < self.value:
            if self.left is not None:
                return self.left.find(value)
        elif value > self.value:
            if self.right is not None:
                return self.right.find(value)
        elif value == self.value:
            return self

    def __contains__(self, value: T):
        if value < self.value:
            return self.left is not None and value in self.left
        elif value > self.value:
            return self.left is not None and value in self.left
        return self.value == value

    def __lt__(self, other: 'BinaryNode[T]'):
        return self.value < other.value

    def __eq__(self, other: 'BinaryNode[T]'):
        return self.value == other.value

    def __repr__(self):
        return f'BinaryNode({self.value})'

    def visit_preorder(self, visit: Callable):
        visit(self.value)
        if self.left: self.left.visit_preorder(visit)
        if self.right: self.right.visit_preorder(visit)

    def is_left_child(self):
        return self.parent is not None and self is self.parent.left

    def is_right_child(self):
        return self.parent is not None and self is self.parent.right

    def _display(self, space: int):
        space += 10

        if self.right: self.right._display(space)
        print()
        for _ in range(10, space):
            print(end=" ")
        print(self.value)
        if self.left: self.left._display(space)

    def print(self):
        self._display(0)

class BinarySearchTree(Generic[T]):
    NODE_TYPE = BinaryNode

    def __init__(self):
        self.root_node = None

    def __contains__(self, value: T) -> bool:
        return self.root_node is not None and value in self.root_node

    def find(self, value: T) -> Optional[BinaryNode[T]]:
        if self.root_node is not None:
            return self.root_node.find(value)

    def insert(self, value: T) -> Optional[BinaryNode[T]]:
        node = None
        if self.root_node is None:
            self.root_node = node = self.NODE_TYPE(value, self)
        else:
            node = self.root_node.insert(value)
        return node

    def delete(self, value: T):
        if self.root_node is not None:
            self.root_node.delete(value)

    def print(self):
        if self.root_node: self.root_node.print()

# colour == True -> Red
# colour == False -> Black
# colour(None) == Black
BLACK = False
RED = True
class ColouredBinaryNode(BinaryNode[T]):
    def __init__(self, *args, colour: bool = RED, **kwargs):
        super().__init__(*args, **kwargs)
        self.colour = colour

    def flip(self):
        self.colour = not self.colour

    def left_rotate(self):
        y = self.right
        self.right = y.left
        if y.left != None:
            y.left.parent = self
        y.parent = self.parent
        if self.parent is None:
            self.tree.root_node = y
        elif self.is_left_child():
            self.parent.left = y
        else:
            self.parent.right = y
        y.left = self
        self.parent = y

    def right_rotate(self):
        # I midlessly swapped left with right from left_rotate
        # Who knows if that's actually correct
        y = self.left
        self.left = y.right
        if y.right != None:
            y.right.parent = self
        y.parent = self.parent
        if self.parent is None:
            self.tree.root_node = y
        elif self.is_right_child():
            self.parent.right = y
        else:
            self.parent.left = y
        y.right = self
        self.parent = y

def _colour(node: Optional[ColouredBinaryNode]) -> bool:
    return node is not None and node.colour

class RedBlackTree(BinarySearchTree[T]):
    NODE_TYPE = ColouredBinaryNode

    def insert(self, value: T):
        node = super().insert(value)

        while _colour(node):
            if node.parent == node.parent.parent.left:
                y = node.parent.parent.right
                if _colour(y):
                    node.parent.colour = BLACK
                    y.colour = BLACK
                    node.parent.parent.colour = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        node.left_rotate()
                    node.parent.colour = BLACK
                    node.parent.parent.colour = RED
                    node.parent.parent.right_rotate()
            else:
                y = node.parent.parent.left
                if _colour(y):
                    node.parent.colour = BLACK
                    y.colour = BLACK
                    node.parent.parent.colour = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        node.right_rotate()
                    node.parent.colour = BLACK
                    node.parent.parent.colour = RED
                    node.parent.parent.left_rotate()

        self.root_node.colour = BLACK


    def delete(self, value: T):
        super().delete(value)
        # TODO: Balance

# t = RedBlackTree()
# t.insert(45)
# t.insert(15)
# t.insert(79)
# t.insert(10)
# t.insert(20)
# t.insert(55)
# t.print()
# print("==============")
# for n in [15, 45, 79, 55, 20, 10]:
#     print('deleting', n)
#     t.delete(n)
#     t.print()
#     print("==============")
