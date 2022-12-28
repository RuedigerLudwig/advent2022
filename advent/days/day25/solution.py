from __future__ import annotations

from typing import Iterator

day_num = 25


def part1(lines: Iterator[str]) -> str:
    snafu = sum(from_snafu(line) for line in lines)
    return to_snafu(snafu)


def part2(lines: Iterator[str]) -> None:
    return None


SNAFU = "=-012"


def from_snafu(line: str) -> int:
    result = 0
    for char in line:
        result = result * 5 + SNAFU.index(char) - 2
    return result


def to_snafu(number: int) -> str:
    result = ""
    while number > 0:
        mod = (number + 2) % 5
        result = SNAFU[mod] + result
        number = (number - mod + 2) // 5
    return result
