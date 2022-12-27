from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from itertools import count, cycle

from typing import Iterator

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


class Direction(Enum):
    North = auto()
    South = auto()
    West = auto()
    East = auto()

    def next(self) -> Direction:
        match self:
            case Direction.North: return Direction.South
            case Direction.South: return Direction.West
            case Direction.West: return Direction.East
            case Direction.East: return Direction.North


@dataclass(slots=True, frozen=True)
class Position:
    x: int
    y: int

    def get_adjacent(self, direction: Direction) -> Iterator[Position]:
        match direction:
            case Direction.North:
                yield Position(self.x - 1, self.y - 1)
                yield Position(self.x, self.y - 1)
                yield Position(self.x + 1, self.y - 1)
            case Direction.South:
                yield Position(self.x - 1, self.y + 1)
                yield Position(self.x, self.y + 1)
                yield Position(self.x + 1, self.y + 1)
            case Direction.West:
                yield Position(self.x - 1, self.y - 1)
                yield Position(self.x - 1, self.y)
                yield Position(self.x - 1, self.y + 1)
            case Direction.East:
                yield Position(self.x + 1, self.y - 1)
                yield Position(self.x + 1, self.y)
                yield Position(self.x + 1, self.y + 1)

    def get_all_adjacent(self) -> Iterator[Position]:
        for y in range(-1, 2):
            for x in range(-1, 2):
                if x != 0 or y != 0:
                    yield Position(self.x + x, self.y + y)

    def walk(self, direction: Direction) -> Position:
        match direction:
            case Direction.North: return Position(self.x, self.y - 1)
            case Direction.South: return Position(self.x, self.y + 1)
            case Direction.West: return Position(self.x - 1, self.y)
            case Direction.East: return Position(self.x + 1, self.y)

    def min(self, other: Position) -> Position:
        return Position(min(self.x, other.x), min(self.y, other.y))

    def max(self, other: Position) -> Position:
        return Position(max(self.x, other.x), max(self.y, other.y))


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
        min_pos = next(iter(self.map))
        max_pos = min_pos
        for elf in self.map:
            min_pos = min_pos.min(elf)
            max_pos = max_pos.max(elf)
        return min_pos, max_pos

    def rounds(self, number: int | None) -> int | None:
        start_dispenser = cycle(iter(Direction))
        if number is None:
            it = count(1)
        else:
            it = range(1, number + 1)

        for n in it:
            start = next(start_dispenser)
            target_map: dict[Position, Position] = {}
            target_count: dict[Position, int] = {}
            for elf in self.map:
                if all(pos not in self.map for pos in elf.get_all_adjacent()):
                    continue

                check_direction = start
                found = False
                while not found:
                    found = True
                    for check in elf.get_adjacent(check_direction):
                        if check in self.map:
                            found = False
                            break

                    if not found:
                        check_direction = check_direction.next()
                        if check_direction == start:
                            found = True
                    else:
                        target = elf.walk(check_direction)
                        target_map[elf] = target
                        target_count[target] = target_count.get(target, 0) + 1

            changed = False
            for from_pos, to_pos in target_map.items():
                if target_count[to_pos] == 1:
                    changed = True
                    self.map.remove(from_pos)
                    self.map.add(to_pos)
            if not changed:
                return n
