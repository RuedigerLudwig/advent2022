from __future__ import annotations
from dataclasses import dataclass
from itertools import cycle

from typing import Iterator, Self

from advent.common.position import Position

day_num = 17


def part1(lines: Iterator[str]) -> int:
    cave = Cave.create(7, next(lines))
    return cave.process_many_rocks(2022)


def part2(lines: Iterator[str]) -> int:
    cave = Cave.create(7, next(lines))
    return cave.process_many_rocks(1_000_000_000_000)


patterns = [["####"],
            [" # ", "###", " # "],
            ["###", "  #", "  #"],
            ["#", "#", "#", "#"],
            ["##", "##"]
            ]


@dataclass(slots=True, frozen=True)
class Pattern:
    lines: list[str]

    @property
    def height(self) -> int:
        return len(self.lines)

    @property
    def width(self) -> int:
        return len(self.lines[0])

    def stones(self, offset: Position) -> Iterator[Position]:
        for y, line in enumerate(self.lines):
            for x, block in enumerate(line):
                if block == "#":
                    yield Position(offset.x + x, offset.y + y)


@dataclass(slots=True)
class Cave:
    width: int
    cave: list[str]
    gas_pushes: Iterator[str]
    rock_dispenser: Iterator[Pattern]

    @property
    def height(self) -> int:
        return len(self.cave)

    def check_free(self, rock: Pattern, position: Position) -> bool:
        for block in rock.stones(position):
            if block.y < len(self.cave) and self.cave[block.y][block.x] == '#':
                return False
        return True

    def fix_rock(self, rock: Pattern, position: Position):
        for _ in range(len(self.cave), position.y + rock.height):
            self.cave.append(' ' * self.width)
        for block in rock.stones(position):
            old = self.cave[block.y]
            self.cave[block.y] = old[:block.x] + '#' + old[block.x + 1:]

    @classmethod
    def create(cls, width: int, gas_pushes: str) -> Self:
        cave = []
        return cls(width, cave, cycle(gas_pushes), cycle(Pattern(pattern) for pattern in patterns))

    def process_one_rock(self) -> tuple[Pattern, Position]:
        rock = next(self.rock_dispenser)
        position = Position(2, len(self.cave) + 3)

        while True:
            match next(self.gas_pushes):
                case '<':
                    next_pos = position.left()
                    if next_pos.x >= 0 and self.check_free(rock, next_pos):
                        position = next_pos
                case '>':
                    next_pos = position.right()
                    if (next_pos.x + rock.width <= self.width
                            and self.check_free(rock, next_pos)):
                        position = next_pos
                case c: raise Exception(f"Illegal char: {c}")

            next_pos = position.up()
            if next_pos.y >= 0 and self.check_free(rock, next_pos):
                position = next_pos
            else:
                self.fix_rock(rock, position)
                return rock, position

    def process_many_rocks(self, max_rounds: int) -> int:
        last_landing_row = 0
        last_max_drop_time = 0
        last_max_drop_height = 0
        last_max_drop_row = 0
        last_max_drop_pattern: Pattern | None = None
        max_drop_height = 0
        time = 0
        added_height = 0
        while time < max_rounds:
            pattern, position = self.process_one_rock()

            if position.y < last_landing_row:
                drop_height = last_landing_row - position.y
                if drop_height == max_drop_height and last_max_drop_pattern == pattern:
                    drop_cycle_height = position.y - last_max_drop_row
                    if last_max_drop_row - drop_cycle_height > 0:
                        different = False
                        for row in range(last_max_drop_row - drop_cycle_height, last_max_drop_row):
                            if self.cave[row] != self.cave[row - drop_cycle_height]:
                                different = True
                                break
                        if not different:
                            time_diff = time - last_max_drop_time
                            height_diff = self.height - last_max_drop_height
                            cycle_count = (max_rounds - time) // time_diff
                            time += cycle_count * time_diff
                            added_height = cycle_count * height_diff
                    last_max_drop_time = time
                    last_max_drop_height = self.height
                    last_max_drop_row = position.y
                elif drop_height > max_drop_height:
                    last_max_drop_time = time
                    last_max_drop_height = self.height
                    last_max_drop_row = position.y
                    last_max_drop_pattern = pattern
                    max_drop_height = drop_height
            last_landing_row = position.y
            time += 1

        return self.height + added_height
