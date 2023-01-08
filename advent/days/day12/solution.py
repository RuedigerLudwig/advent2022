from __future__ import annotations
from dataclasses import dataclass
from queue import Queue

from typing import Iterator, Self

from advent.common.position import ORIGIN, Position

day_num = 12


def part1(lines: Iterator[str]) -> int:
    return Map.create(lines).find_path('S')


def part2(lines: Iterator[str]) -> int:
    return Map.create(lines).find_path('a')


@dataclass(slots=True, frozen=True)
class Map:
    map: list[str]
    bottom_right: Position

    @classmethod
    def create(cls, input: Iterator[str]) -> Self:
        map = list(input)
        width = len(map[0])
        height = len(map)
        return Map(map, Position(width, height))

    def can_climb(self, *, from_pos: Position, to_pos: Position) -> bool:
        """ Checks if one gan walk from the elevation at from_pos to the elevation at to_pos """
        from_elevation = self.get_elevation(from_pos)
        to_elevation = self.get_elevation(to_pos)
        if to_elevation == 'E':
            return from_elevation >= 'y'

        if from_elevation == 'S':
            return to_elevation <= 'b'

        return ord(to_elevation) <= ord(from_elevation) + 1

    def get_elevation(self, position: Position) -> str:
        """ returns the elevation at the given position """
        return self.map[position.y][position.x]

    def find_marker(self, point: str) -> Position:
        """ Returns the position of the first marker matching the argument """
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == point:
                    return Position(x, y)

        raise Exception(f"Did not find point {point}")

    def find_path(self, target: str):
        """ Finds a path backwards from the Endpoint to an elevation/marker target """
        endpoint = self.find_marker('E')
        found: set[Position] = {endpoint}
        queue: Queue[tuple[int, Position]] = Queue()
        queue.put((0, endpoint))
        while not queue.empty():
            current_len, current_pos = queue.get()
            for next_position in self.next_step(current_pos):
                if next_position not in found:
                    elevation = self.get_elevation(next_position)
                    if elevation == target:
                        return current_len + 1
                    found.add(next_position)
                    queue.put((current_len + 1, next_position))
        raise Exception('No Path found')

    def next_step(self, current_pos: Position) -> Iterator[Position]:
        """ yields all neighbors, that could have been the previous step to this one"""
        for neighbor in current_pos.unit_neighbors():
            if (neighbor.is_within(ORIGIN, self.bottom_right)
                    and self.can_climb(from_pos=neighbor, to_pos=current_pos)):
                yield neighbor
