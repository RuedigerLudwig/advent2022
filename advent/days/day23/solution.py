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

    def count_adjacent(self, elves: dict[Position, int],
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
        it = iter(self.map)
        min_pos = next(it)
        max_pos = min_pos
        for elf in it:
            min_pos = min_pos.component_min(elf)
            max_pos = max_pos.component_max(elf)
        return min_pos, max_pos

    def rounds(self, number: int | None) -> int | None:
        start_dispenser = cycle(iter(Direction))
        if number is None:
            it = count(1)
        else:
            it = range(1, number + 1)

        elves = {position: -1 for position in self.map}

        min_moved, max_moved = self.extent()

        for n in it:
            min_moved = min_moved + Position(-2, -2)
            max_moved = max_moved + Position(2, 2)
            start = next(start_dispenser)
            target_map: dict[Position, Position] = {}
            for from_pos, last_moved in elves.items():
                if last_moved + 4 <= n:
                    if not from_pos.is_within(min_moved, max_moved):
                        continue

                adjacent = self.count_adjacent(elves, from_pos)
                if adjacent is None:
                    continue

                next_direction = start
                while True:
                    if next_direction in adjacent:
                        next_direction = next_direction.next()
                    else:
                        target = next_direction.walk(from_pos)
                        if target not in target_map:
                            target_map[target] = from_pos
                        else:
                            del target_map[target]
                        break

            changed = False
            first = True
            for to_pos, from_pos in target_map.items():
                changed = True
                del elves[from_pos]
                elves[to_pos] = n
                if first:
                    max_moved = to_pos
                    min_moved = to_pos
                    first = False
                else:
                    max_moved = max_moved.component_max(to_pos, from_pos)
                    min_moved = min_moved.component_min(to_pos, from_pos)

            if not changed:
                self.map = {elf for elf in elves}
                return n

        self.map = {elf for elf in elves}
        return None
