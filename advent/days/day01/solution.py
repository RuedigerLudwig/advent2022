from __future__ import annotations

from typing import Iterator

day_num = 1


def part1(lines: Iterator[str]) -> int:
    return max(parse_carried_food(lines))


def part2(lines: Iterator[str]) -> int:
    return sum(sorted(parse_carried_food(lines))[-3:])


def parse_carried_food(lines: Iterator[str]) -> Iterator[int]:
    """
    Parses lines of string as integers and returns the sum of blocks separated by blank lines

    Parameters
    ----------
    lines : Iterator[str]
      The lines to be parsed

    Returns
    -------
    Iterator[int]
      An iterator for the calories carried by each elf

    Raises
    ------
    ValueError
      If a line is neither empty nor represents a valid int
    """

    calories = 0
    for line in lines:
        if line:
            calories += int(line)
        else:
            yield calories
            calories = 0

    if calories != 0:
        yield calories
