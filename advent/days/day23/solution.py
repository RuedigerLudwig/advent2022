from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from itertools import count, cycle

from typing import Iterable, Iterator

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
    def check_adjacent(cls, elves: Iterable[Position],
                       position: Position) -> list[Direction] | None:
        north = False
        south = False
        west = False
        east = False

        if (position + Position(-1, -1)) in elves:
            north = True
            west = True
        if (position + Position(1, 1)) in elves:
            south = True
            east = True

        if north is False:
            north = (position + Position(0, -1)) in elves
        if south is False:
            south = (position + Position(0, 1)) in elves
        if west is False:
            west = (position + Position(-1, 0)) in elves
        if east is False:
            east = (position + Position(1, 0)) in elves

        if north is False or east is False:
            if (position + Position(1, -1)) in elves:
                north = True
                east = True
        if south is False or west is False:
            if (position + Position(-1, 1)) in elves:
                south = True
                west = True

        if north == south == east == west:
            return None

        adjacent: list[Direction] = []
        if north:
            adjacent.append(Direction.North)
        if south:
            adjacent.append(Direction.South)
        if west:
            adjacent.append(Direction.West)
        if east:
            adjacent.append(Direction.East)

        return adjacent

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

    def rounds(self, max_rounds: int | None) -> int | None:
        start_dispenser = cycle(iter(Direction))
        if max_rounds is None:
            it = count(1)
        else:
            it = range(1, max_rounds + 1)

        elves = {position: 0 for position in self.map}

        min_position, max_position = self.extent()

        for round in it:
            min_position = min_position + Position(-1, -1)
            max_position = max_position + Position(1, 1)
            start = next(start_dispenser)
            proposals: dict[Position, Position] = {}
            for from_pos, last_moved in elves.items():
                if last_moved + 4 < round:
                    if not from_pos.is_within(min_position, max_position):
                        continue

                adjacent = self.check_adjacent(elves, from_pos)
                if adjacent is None:
                    continue

                next_direction = start
                while True:
                    if next_direction in adjacent:
                        next_direction = next_direction.next()
                    else:
                        to_pos = next_direction.walk(from_pos)
                        if to_pos not in proposals:
                            proposals[to_pos] = from_pos
                        else:
                            del proposals[to_pos]
                        break

            if not proposals:
                self.map = set(elves)
                return round

            first = True
            for to_pos, from_pos in proposals.items():
                del elves[from_pos]
                elves[to_pos] = round

                if first:
                    max_position = Position.component_max(to_pos, from_pos)
                    min_position = Position.component_min(to_pos, from_pos)
                    first = False
                else:
                    max_position = Position.component_max(max_position, to_pos, from_pos)
                    min_position = Position.component_min(min_position, to_pos, from_pos)

        self.map = set(elves)
        return None
