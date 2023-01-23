from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from itertools import count, cycle

from typing import Iterator

from advent.common.position import Position

day_num = 23


def part1(lines: Iterator[str]) -> int:
    ground = Ground.parse(lines)
    ground.rounds(10)
    return ground.count_empty()


def part2(lines: Iterator[str]) -> int:
    ground = Ground.parse(lines)
    result = ground.rounds(None)
    if result is None:
        assert False, "Unreachable"
    return result


class Direction(IntEnum):
    North = 0
    South = 1
    West = 2
    East = 3

    def next(self) -> Direction:
        return Direction((self + 1) % 4)

    def walk(self, position: Position) -> Position:
        match self:
            case Direction.North: return Position(position.x, position.y - 1)
            case Direction.South: return Position(position.x, position.y + 1)
            case Direction.West: return Position(position.x - 1, position.y)
            case Direction.East: return Position(position.x + 1, position.y)


@dataclass(slots=True)
class Ground:
    map: set[Position]

    def __str__(self) -> str:
        min_pos, max_pos = self.extent()
        result = ""
        for y in range(min_pos.y, max_pos.y + 1):
            for x in range(min_pos.x, max_pos.x + 1):
                if Position(x, y) in self.map:
                    result += '#'
                else:
                    result += '.'
            result += '\n'
        return result[:-1]

    @classmethod
    def has_neighbor(cls, elves: dict[Position, int],
                     position: Position, direction: Direction) -> bool:
        match direction:
            case Direction.North:
                return (
                    Position(position.x - 1, position.y - 1) in elves
                    or Position(position.x, position.y - 1) in elves
                    or Position(position.x + 1, position.y - 1) in elves
                )
            case Direction.South:
                return (
                    Position(position.x - 1, position.y + 1) in elves
                    or Position(position.x, position.y + 1) in elves
                    or Position(position.x + 1, position.y + 1) in elves
                )
            case Direction.West:
                return (
                    Position(position.x - 1, position.y - 1) in elves
                    or Position(position.x - 1, position.y) in elves
                    or Position(position.x - 1, position.y + 1) in elves
                )
            case Direction.East:
                return (
                    Position(position.x + 1, position.y - 1) in elves
                    or Position(position.x + 1, position.y) in elves
                    or Position(position.x + 1, position.y + 1) in elves
                )

    def count_empty(self) -> int:
        min_pos, max_pos = self.extent()
        return (max_pos.x - min_pos.x + 1) * (max_pos.y - min_pos.y + 1) - len(self.map)

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Ground:
        map: set[Position] = set()
        for y, line in enumerate(lines):
            for x, tile in enumerate(line):
                if tile == '#':
                    map.add(Position(x, y))
        return Ground(map)

    def extent(self) -> tuple[Position, Position]:
        return Position.component_min(*self.map), Position.component_max(*self.map)

    @classmethod
    def minmax(cls, first: int, second: int) -> tuple[int, int]:
        return (first, second) if first <= second else (second, first)

    @classmethod
    def pair_neighbors(cls, from_pos: Position, to_pos: Position) -> Iterator[Position]:
        if from_pos.x == to_pos.x:
            mn, mx = Ground.minmax(from_pos.y, to_pos.y)
            yield Position(from_pos.x - 1, mn - 1)
            yield Position(from_pos.x, mn - 1)
            yield Position(from_pos.x + 1, mn - 1)
            yield Position(from_pos.x - 1, from_pos.y)
            yield Position(from_pos.x + 1, from_pos.y)
            yield Position(from_pos.x - 1, mx + 1)
            yield Position(from_pos.x, mx + 1)
            yield Position(from_pos.x + 1, mx + 1)
        else:
            mn, mx = Ground.minmax(from_pos.x, to_pos.x)
            yield Position(mn - 1, from_pos.y - 1)
            yield Position(mn - 1, from_pos.y)
            yield Position(mn - 1, from_pos.y + 1)
            yield Position(from_pos.x, from_pos.y - 1)
            yield Position(from_pos.x, from_pos.y + 1)
            yield Position(mx + 1, from_pos.y - 1)
            yield Position(mx + 1, from_pos.y)
            yield Position(mx + 1, from_pos.y + 1)

    def rounds(self, max_rounds: int | None) -> int | None:
        start_dispenser = cycle(iter(Direction))
        if max_rounds is None:
            it = count(1)
        else:
            it = range(1, max_rounds + 1)

        elves = {position: 0 for position in self.map}

        for round in it:
            start = next(start_dispenser)
            proposals: dict[Position, Position] = {}
            touched: set[Position] = set()
            for from_pos, last_touched in elves.items():
                if last_touched + 4 < round:
                    continue

                found = False
                for neighbor in from_pos.all_neighbors():
                    if neighbor in elves:
                        found = True
                        break

                if not found:
                    continue

                next_direction = start
                found = True
                while Ground.has_neighbor(elves, from_pos, next_direction):
                    next_direction = next_direction.next()
                    if next_direction == start:
                        found = False
                        break

                if found:
                    to_pos = next_direction.walk(from_pos)
                    old_from = proposals.pop(to_pos, None)
                    if old_from is None:
                        proposals[to_pos] = from_pos
                    else:
                        touched.add(from_pos)
                        touched.add(old_from)

            if not proposals:
                self.map = set(elves)
                return round

            for to_pos, from_pos in proposals.items():
                elves[to_pos] = round
                del elves[from_pos]

                for neighbor in Ground.pair_neighbors(from_pos, to_pos):
                    if neighbor in elves:
                        elves[neighbor] = round

            for touched_pos in touched:
                elves[touched_pos] = round

        self.map = set(elves)
        return None
