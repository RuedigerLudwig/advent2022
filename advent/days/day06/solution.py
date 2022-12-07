from __future__ import annotations

from itertools import combinations
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
        found = False
        for a, b in combinations(line[pos - length:pos], 2):
            if a == b:
                found = True
                break
        if not found:
            return pos

    raise Exception("No marker found")
