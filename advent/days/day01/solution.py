from __future__ import annotations

from typing import Iterator, Generator

day_num = 1


def part1(lines: Iterator[str]) -> int:
    return max(parse_lines(lines))


def part2(lines: Iterator[str]) -> int:
    return sum(sorted(parse_lines(lines))[-3:])


def parse_lines(lines: Iterator[str]) -> Generator[int, None, None]:
    """
    Parses lines of string as integers and returns the sum of blocks separated by blank lines

    Parameters
    ----------
    lines : Iterator[str]
      The lines to be parsed

    Returns
    -------
    Generator[int, None, None]
      A generator for the sum of each block

    Raises
    ------
    ValueError
      If a line is neither empty nor represents a valid int
    """
    current = 0

    for line in lines:
        if line:
            current += int(line)
        else:
            yield current
            current = 0

    if current != 0:
        yield current
