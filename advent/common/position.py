from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator, Literal


@dataclass(slots=True, frozen=True, order=True)
class Position:
    x: int
    y: int

    def __getitem__(self, index: Literal[0, 1]) -> int:
        match index:
            case 0: return self.x
            case 1: return self.y
            case _: raise IndexError()

    def __iter__(self) -> Iterator[int]:
        yield self.x
        yield self.y

    def set_x(self, x: int) -> Position:
        return Position(x, self.y)

    def set_y(self, y: int) -> Position:
        return Position(self.x, y)

    def __neg__(self) -> Position:
        return Position(-self.x, -self.y)

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, factor: int) -> Position:
        return Position(self.x * factor, self.y * factor)

    def taxicab_distance(self, other: Position | None = None) -> int:
        if other is None:
            return abs(self.x) + abs(self.y)
        else:
            return abs(self.x - other.x) + abs(self.y - other.y)

    def right(self) -> Position:
        return Position(self.x + 1, self.y)

    def up(self) -> Position:
        return Position(self.x, self.y - 1)

    def left(self) -> Position:
        return Position(self.x - 1, self.y)

    def down(self) -> Position:
        return Position(self.x, self.y + 1)

    def unit_neighbors(self) -> Iterator[Position]:
        yield self.right()
        yield self.up()
        yield self.left()
        yield self.down()

    def is_within(self, top_left: Position, bottom_right: Position) -> bool:
        return top_left.x <= self.x < bottom_right.x and top_left.y <= self.y < bottom_right.y


ORIGIN = Position(0, 0)
UNIT_X = Position(1, 0)
UNIT_Y = Position(0, 1)
UNIT_NEG_X = Position(-1, 0)
UNIT_NEG_Y = Position(0, -1)
