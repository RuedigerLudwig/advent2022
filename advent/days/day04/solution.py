from __future__ import annotations
from dataclasses import dataclass

from typing import Iterator, Self

day_num = 4


def part1(lines: Iterator[str]) -> int:
    return sum(1 for line in lines if Pair.parse(line).includes())


def part2(lines: Iterator[str]) -> int:
    return sum(1 for line in lines if Pair.parse(line).overlap())


@dataclass(slots=True, frozen=True)
class Range:
    start: int
    end: int

    @classmethod
    def parse(cls, line: str) -> Self:
        match line.split('-'):
            case [s, e]: return cls(int(s), int(e))
            case _: raise Exception(f"Not a valid range: {line}")

    def includes(self, other: Range) -> bool:
        """ Check if this range includes the other """
        return self.start <= other.start and self.end >= other.end

    def overlap(self, other: Range) -> bool:
        """ Check if this range obverlaps with the other """
        return self.start <= other.end and other.start <= self.end


@dataclass(slots=True, frozen=True)
class Pair:
    first: Range
    second: Range

    @classmethod
    def parse(cls, line: str) -> Self:
        match line.split(','):
            case [f, s]: return cls(Range.parse(f), Range.parse(s))
            case _: raise Exception(f"Not a valid Pair: {line}")

    def includes(self) -> bool:
        """ Check if one range includes the other """
        return self.first.includes(self.second) or self.second.includes(self.first)

    def overlap(self) -> bool:
        """ Check if the two ranges obverlap """
        return self.first.overlap(self.second)
