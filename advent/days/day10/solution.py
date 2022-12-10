from __future__ import annotations

from typing import Iterator

day_num = 10


def part1(lines: Iterator[str]) -> int:
    return sum(grab_values(lines))


def part2(lines: Iterator[str]) -> list[str]:
    return draw(lines, 40, 6)


def parse(line: str) -> None | int:
    """
    Parses the a line into the two possible instructions.
    May raise if the instructions was invalid
    """
    match line.split():
        case ['noop']:
            return None
        case ['addx', value]:
            return int(value)
        case _:
            raise Exception(f"Unknown line: {line}")


def cycles(lines: Iterator[str]) -> Iterator[int]:
    """
    Cycles through the instructions and yields a new value for each cycle
    """
    register = 1
    for line in lines:
        yield register
        match parse(line):
            case None:
                pass
            case value:
                yield register
                register += value
    yield register


def grab_values(lines: Iterator[str]) -> Iterator[int]:
    for cycle, value in enumerate(cycles(lines), start=1):
        if cycle in [20, 60, 100, 140, 180, 220]:
            yield cycle * value


def draw(lines: Iterator[str], width: int, height: int) -> list[str]:
    picture = ""
    for cycle, sprite in enumerate(cycles(lines)):
        crt_pos = cycle % width
        if sprite - 1 <= crt_pos and crt_pos <= sprite + 1:
            picture += '#'
        else:
            picture += ' '

        if crt_pos == width - 1:
            picture += '\n'
    return picture.split('\n')[:height]
