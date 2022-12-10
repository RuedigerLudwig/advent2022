from __future__ import annotations
from dataclasses import dataclass

from typing import Iterator, Self

day_num = 9


def part1(lines: Iterator[str]) -> int:
    commands = (Command.parse(line) for line in lines)
    return simulate(commands, 2)


def part2(lines: Iterator[str]) -> int:
    commands = (Command.parse(line) for line in lines)
    return simulate(commands, 10)


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int

    @classmethod
    def parse_direction(cls, char: str) -> Self:
        """ Parses the given direction to a Point. May raise if invalid """
        match char:
            case 'R':
                return cls(1, 0)
            case 'U':
                return cls(0, 1)
            case 'L':
                return cls(-1, 0)
            case 'D':
                return cls(0, -1)
            case _:
                raise Exception(f"Unkown Direction: {char}")

    def add(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def sub(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def is_unit(self) -> bool:
        """ return true, if this describes any point (diagonally) adjacent to the origin"""
        return abs(self.x) <= 1 and abs(self.y) <= 1

    def as_unit(self) -> Point:
        """ Compresses this Point to a point with unit components """
        def unit(num: int) -> int:
            return 0 if num == 0 else num // abs(num)
        return Point(unit(self.x), unit(self.y))

    def step_to(self, other: Point) -> Point | None:
        """ Returns a point one step towards the other point. Returns None, if already adjacent """
        diff = other.sub(self)
        if diff.is_unit():
            return None
        return self.add(diff.as_unit())


@dataclass(frozen=True, slots=True)
class Command:
    dir: Point
    steps: int

    @classmethod
    def parse(cls, line: str) -> Self:
        """ Parse a command line. My raise exception if the was an illegal line"""
        match line.split():
            case [dir, steps]:
                return Command(Point.parse_direction(dir), int(steps))
            case _:
                raise Exception(f"Illegal line: {line}")


def simulate(lst: Iterator[Command], rope_length: int) -> int:
    """ Walks the whole rope in Planck length steps according to commands """
    rope = [Point(0, 0)] * rope_length
    visited = {rope[-1]}
    for command in lst:
        for _ in range(command.steps):
            rope[0] = rope[0].add(command.dir)
            for n in range(1, rope_length):
                moved_piece = rope[n].step_to(rope[n - 1])
                if not moved_piece:
                    break
                rope[n] = moved_piece
                if n == rope_length - 1:
                    visited.add(rope[n])

    return len(visited)
