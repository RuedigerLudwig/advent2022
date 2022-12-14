from __future__ import annotations
from dataclasses import dataclass
from itertools import count

from typing import Iterator, Self

day_num = 14


def part1(lines: Iterator[str]) -> int:
    cave = BottomLessCave.create(lines)
    return cave.drip_till_forever()


def part2(lines: Iterator[str]) -> int:
    cave = FlooredCave.create(lines, floor=2)
    return cave.drip_till_full()


@dataclass(slots=True)
class CaveMap:
    filled: set[tuple[int, int]]
    max_depths: int

    def is_filled(self, pos: tuple[int, int]) -> bool:
        return pos in self.filled

    def set_filled(self, pos: tuple[int, int]):
        self.filled.add(pos)

    @classmethod
    def get_map(cls, lines: Iterator[str], add_floor: int) -> Self:
        rocks: set[tuple[int, int]] = set()
        for line in lines:
            path = cls.parse_rock_path(line)
            current = path[0]
            rocks.add(current)
            for next in path[1:]:
                rocks.update(cls.get_path(current, next))
                current = next
        return CaveMap(rocks, max(y for _, y in rocks) + add_floor)

    @classmethod
    def get_path(cls, from_pos: tuple[int, int],
                 to_pos: tuple[int, int]) -> Iterator[tuple[int, int]]:
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        if from_x == to_x:
            if from_y < to_y:
                return ((from_x, y) for y in range(from_y + 1, to_y + 1))
            else:
                return ((from_x, y) for y in range(from_y - 1, to_y - 1, -1))
        elif from_x < to_x:
            return ((x, from_y) for x in range(from_x + 1, to_x + 1))
        else:
            return ((x, from_y) for x in range(from_x - 1, to_x - 1, -1))

    @classmethod
    def parse_rock_path(cls, line: str) -> list[tuple[int, int]]:
        return [(int(x.strip()), int(y.strip()))
                for x, y in (part.split(',') for part in line.split('->'))]

    def next_free(self, pos: tuple[int, int]) -> tuple[int, int] | None:
        pos_x, pos_y = pos
        if not self.is_filled((pos_x, pos_y + 1)):
            return pos_x, pos_y + 1
        if not self.is_filled((pos_x - 1, pos_y + 1)):
            return pos_x - 1, pos_y + 1
        if not self.is_filled((pos_x + 1, pos_y + 1)):
            return pos_x + 1, pos_y + 1
        return None


@dataclass
class BottomLessCave:
    cave_map: CaveMap

    @classmethod
    def create(cls, lines: Iterator[str]) -> Self:
        cave_map = CaveMap.get_map(lines, 0)
        return BottomLessCave(cave_map)

    def drip(self) -> bool:
        origin = 500, 0
        if self.cave_map.is_filled(origin):
            return False

        while True:
            next_pos = self.cave_map.next_free(origin)
            if next_pos is None:
                self.cave_map.set_filled(origin)
                return True
            if next_pos[1] == self.cave_map.max_depths:
                return False
            origin = next_pos

    def drip_till_forever(self) -> int:
        for round in count():
            if not self.drip():
                return round
        assert False, "Unreachable"


@dataclass
class FlooredCave:
    cave_map: CaveMap

    @classmethod
    def create(cls, lines: Iterator[str], floor: int) -> Self:
        return FlooredCave(CaveMap.get_map(lines, floor))

    def drip_till_full(self) -> int:
        count = 1
        line: set[tuple[int, int]] = {(500, 0)}
        for _ in range(self.cave_map.max_depths - 1):
            next_line: set[tuple[int, int]] = set()
            for x, y in line:
                if not self.cave_map.is_filled((x - 1, y + 1)):
                    next_line.add((x - 1, y + 1))
                if not self.cave_map.is_filled((x, y + 1)):
                    next_line.add((x, y + 1))
                if not self.cave_map.is_filled((x + 1, y + 1)):
                    next_line.add((x + 1, y + 1))
            count += len(next_line)
            line = next_line
        return count
