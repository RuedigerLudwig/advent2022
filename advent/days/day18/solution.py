from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from typing import Iterable, Iterator, Self

day_num = 18


def part1(lines: Iterator[str]) -> int:
    shower = Shower.create(Position3D.parse_all(lines))
    return shower.faces


def part2(lines: Iterator[str]) -> int:
    shower = Shower.create(Position3D.parse_all(lines))
    return shower.faces - shower.count_trapped_droplets()


@dataclass(slots=True, frozen=True)
class Position3D:
    x: int
    y: int
    z: int

    @classmethod
    def parse(cls, line: str) -> Self:
        x, y, z = line.split(",")
        return Position3D(int(x), int(y), int(z))

    @classmethod
    def parse_all(cls, lines: Iterable[str]) -> Iterator[Self]:
        return (cls.parse(line) for line in lines)

    def neighbors(self) -> Iterator[Position3D]:
        yield Position3D(self.x + 1, self.y, self.z)
        yield Position3D(self.x - 1, self.y, self.z)
        yield Position3D(self.x, self.y + 1, self.z)
        yield Position3D(self.x, self.y - 1, self.z)
        yield Position3D(self.x, self.y, self.z + 1)
        yield Position3D(self.x, self.y, self.z - 1)

    def min_max(self, mm: tuple[Position3D, Position3D] | None) -> tuple[Position3D, Position3D]:
        if mm is None:
            return self, self

        return (Position3D(min(mm[0].x, self.x),
                           min(mm[0].y, self.y),
                           min(mm[0].z, self.z)),
                Position3D(max(mm[1].x, self.x),
                           max(mm[1].y, self.y),
                           max(mm[1].z, self.z)))

    def is_between(self, min: Position3D, max: Position3D) -> bool:
        return (min.x <= self.x <= max.x
                and min.y <= self.y <= max.y
                and min.z <= self.z <= max.z)


class DropletType(Enum):
    DROP = 1
    UNKNOWN = 2
    OUTER = 3


@dataclass(slots=True, frozen=True)
class Shower:
    droplets: dict[Position3D, tuple[DropletType, int]]
    faces: int

    @classmethod
    def create(cls, positions: Iterable[Position3D]) -> Self:
        droplets: dict[Position3D, tuple[DropletType, int]] = {}
        faces = 0
        for position in positions:
            candidate = droplets.get(position)
            if candidate is not None:
                _, touching_faces = candidate
            else:
                touching_faces = 0

            faces += 6
            for neighbor in position.neighbors():
                candidate = droplets.get(neighbor)
                if candidate is not None:
                    droplet_type, neighbor_touching_faces = candidate
                    if droplet_type == DropletType.DROP:
                        touching_faces += 1
                        faces -= 2
                    droplets[neighbor] = droplet_type, neighbor_touching_faces + 1
                else:
                    droplets[neighbor] = DropletType.UNKNOWN, 1
            droplets[position] = DropletType.DROP, touching_faces
        return Shower(droplets, faces)

    def count_trapped_droplets(self) -> int:
        droplets = self.droplets.copy()
        minmax: tuple[Position3D, Position3D] | None = None
        for position in droplets.keys():
            minmax = position.min_max(minmax)
        if minmax is None:
            raise Exception("I got no data to work with")
        min_values, max_values = minmax

        todo: list[Position3D] = [min_values]
        while todo:
            current = todo[0]
            todo = todo[1:]

            candidate = droplets.get(current)

            skip_further = True
            if candidate is None:
                droplets[current] = DropletType.OUTER, 0
                skip_further = False
            else:
                droplet_type, faces = candidate
                if droplet_type == DropletType.UNKNOWN:
                    droplets[current] = DropletType.OUTER, faces
                    skip_further = False

            if not skip_further:
                for neighbor in current.neighbors():
                    if neighbor.is_between(min_values, max_values):
                        todo.append(neighbor)

        return sum(touching_faces
                   for droplet_type, touching_faces in droplets.values()
                   if droplet_type == DropletType.UNKNOWN)
