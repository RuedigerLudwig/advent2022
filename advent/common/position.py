from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator, Literal


@dataclass(slots=True, frozen=True, order=True)
class Position:
    """ This class represents a position in 2D integer space """
    x: int
    y: int

    @classmethod
    def splat(cls, value: int) -> Position:
        """ Creates a Position with two equal values """
        return cls(value, value)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __getitem__(self, index: Literal[0, 1]) -> int:
        """ Gets the first or second component of this position """
        match index:
            case 0: return self.x
            case 1: return self.y
            case _: raise IndexError()

    def __iter__(self) -> Iterator[int]:
        """ Iterates over all components of this psition """
        yield self.x
        yield self.y

    def set_x(self, x: int) -> Position:
        """ Creates a copy of this position with x set to the new value """
        return Position(x, self.y)

    def set_y(self, y: int) -> Position:
        """ Creates a copy of this position with y set to the new value """
        return Position(self.x, y)

    def __neg__(self) -> Position:
        """ Creates a copy of this position with all values negated """
        return Position(-self.x, -self.y)

    def __add__(self, other: Position) -> Position:
        """ Adds the components of these two positions """
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        """ Subtracts the components of these two positions """
        return Position(self.x - other.x, self.y - other.y)

    def __mul__(self, factor: int) -> Position:
        """ Multiplies all components of this position by the given factor """
        return Position(self.x * factor, self.y * factor)

    def right(self) -> Position:
        """ Returns the neighboring position to the right """
        return self + UNIT_X

    def up(self) -> Position:
        """ Returns the neighboring position above """
        return self + UNIT_NEG_Y

    def left(self) -> Position:
        """ Returns the neighboring position to the left """
        return self + UNIT_NEG_X

    def down(self) -> Position:
        """ Returns the neighboring position below """
        return self + UNIT_Y

    def unit_neighbors(self) -> Iterator[Position]:
        """ Returns an iterator of all direct neighbors """
        yield self.right()
        yield self.up()
        yield self.left()
        yield self.down()

    def all_neighbors(self) -> Iterator[Position]:
        yield Position(self.x + 1, self.y)
        yield Position(self.x + 1, self.y - 1)
        yield Position(self.x, self.y - 1)
        yield Position(self.x - 1, self.y - 1)
        yield Position(self.x - 1, self.y)
        yield Position(self.x - 1, self.y + 1)
        yield Position(self.x, self.y + 1)
        yield Position(self.x + 1, self.y + 1)

    def is_within(self, top_left: Position, bottom_right: Position) -> bool:
        """
        Checks if this point is within the rectangle spanned by the given positions.
        Behavior is undefined if top_left and bottom_right are not in the correct order.
        """
        return top_left.x <= self.x <= bottom_right.x and top_left.y <= self.y <= bottom_right.y

    def taxicab_distance(self, other: Position | None = None) -> int:
        """
        If other is given returns the taxicab distance from this point to other.
        Otherwise returns the taxicab distance of this position to the Origin.
        """
        if other is None:
            return abs(self.x) + abs(self.y)
        else:
            return abs(self.x - other.x) + abs(self.y - other.y)

    @classmethod
    def component_min(cls, *positions: Position) -> Position:
        """
        Returns the position with the minimal value for each component
        Basically this gives the top left corner of the square that
        includes all given positions
        """
        it = iter(positions)
        best = next(it)
        for pos in it:
            if best.x <= pos.x and best.y <= pos.y:
                pass
            elif best.x >= pos.x and best.y >= pos.y:
                best = pos
            else:
                best = Position(min(best.x, pos.x), min(best.y, pos.y))
        return best

    @classmethod
    def component_max(cls, *positions: Position) -> Position:
        """
        Returns the position with the maximum value for each component
        Basically this gives the bottom right corner of the square that
        includes all given positions
        """
        it = iter(positions)
        best = next(it)
        for pos in it:
            if best.x >= pos.x and best.y >= pos.y:
                pass
            elif best.x <= pos.x and best.y <= pos.y:
                best = pos
            else:
                best = Position(max(best.x, pos.x), max(best.y, pos.y))
        return best


ORIGIN = Position.splat(0)
UNIT_X = Position(1, 0)
UNIT_Y = Position(0, 1)
UNIT_NEG_X = Position(-1, 0)
UNIT_NEG_Y = Position(0, -1)
