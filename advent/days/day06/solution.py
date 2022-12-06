from __future__ import annotations

from itertools import product
from typing import Iterator

day_num = 6


def part1(lines: Iterator[str]) -> int:
    return marker(next(lines), 4)


def part2(lines: Iterator[str]) -> int:
    return marker(next(lines), 14)


def marker(line: str, length: int) -> int:
    """
    Returns the position just after a marker. A marker has [length] non repeated characters.
    Raises Exception if no marker was found
    """
    for pos in range(length, len(line)):
        identical = 0
        for a, b in product(line[pos - length:pos], repeat=2):
            if a == b:
                identical += 1
        if identical == length:
            return pos

    raise Exception("No marker found")
