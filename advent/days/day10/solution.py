from __future__ import annotations

from typing import Iterator

day_num = 10


def part1(lines: Iterator[str]) -> int:
    return sum(Signal.grab_values(lines))


def part2(lines: Iterator[str]) -> list[str]:
    return Signal.draw(lines, 40, 6)


class Signal:
    @staticmethod
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

    @staticmethod
    def cycles(lines: Iterator[str]) -> Iterator[int]:
        """
        Cycles throw the instructions and yields a new value on each cycle
        """
        register = 1
        for line in lines:
            yield register
            command = Signal.parse(line)
            if command is not None:
                yield register
                register += command

    @staticmethod
    def grab_values(lines: Iterator[str]) -> Iterator[int]:
        for cycle, value in enumerate(Signal.cycles(lines), start=1):
            if cycle in [20, 60, 100, 140, 180, 220]:
                yield cycle * value

    @staticmethod
    def draw(lines: Iterator[str], width: int, height: int) -> list[str]:
        picture = ""
        for cycle, sprite in enumerate(Signal.cycles(lines)):
            crt_pos = cycle % width
            if sprite - 1 <= crt_pos and crt_pos <= sprite + 1:
                picture += '#'
            else:
                picture += ' '

            if crt_pos == width - 1:
                picture += '\n'
        return picture.split('\n')[:height]
