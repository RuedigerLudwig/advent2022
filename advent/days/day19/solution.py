from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from itertools import islice
from math import prod
from queue import PriorityQueue

from typing import Iterator, Self
from advent.parser.parser import P

day_num = 19


def part1(lines: Iterator[str]) -> int:
    return sum(blueprint.number * blueprint.run(24)
               for blueprint in (Blueprint.parse(line) for line in lines))


def part2(lines: Iterator[str]) -> int:
    return prod(Blueprint.parse(line).run(32) for line in islice(lines, 3))


number_parser = P.second(P.string("Blueprint "), P.unsigned())
ore_parser = P.second(P.string(": Each ore robot costs "), P.unsigned())
clay_parser = P.second(P.string(" ore. Each clay robot costs "), P.unsigned())
tuple_parser = P.seq(P.unsigned(), P.second(P.string(" ore and "), P.unsigned()))
obsidian_parser = P.second(P.string(" ore. Each obsidian robot costs "), tuple_parser)
geode_parser = P.second(P.string(" clay. Each geode robot costs "), tuple_parser)
blueprint_parser = P.map5(number_parser, ore_parser, clay_parser, obsidian_parser, geode_parser,
                          lambda number, ore, clay, obsidian, geode:
                          Blueprint.create(number, ore, clay, obsidian, geode))


class Element(IntEnum):
    Geode = 0
    Obsidian = 1
    Clay = 2
    Ore = 3


Elements = tuple[int, int, int, int]


def gt(first: Elements, second: Elements) -> bool:
    return all(f >= s for f, s in zip(first, second))


def add(first: Elements, second: Elements) -> Elements:
    return tuple(v1 + v2 for v1, v2 in zip(first, second))


def sub(first: Elements, second: Elements) -> Elements:
    return Elements(tuple(v1 - v2 for v1, v2 in zip(first, second)))


def inc_tuple(elements: Elements, pos: Element) -> Elements:
    return tuple(v + 1 if num == pos else v for num, v in enumerate(elements))


@dataclass(slots=True)
class Path:
    time: int
    material: Elements
    robots: Elements
    blueprint: Blueprint
    path: list[Element | None]

    @classmethod
    def start(cls, blueprint: Blueprint) -> Path:
        return Path(0, (0, 0, 0, 0), (0, 0, 0, 1), blueprint, [])

    def _check(self, element: Element) -> Path | None:
        if gt(self.material, self.blueprint.requirements[element]):
            return Path(self.time + 1,
                        add(sub(self.material, self.blueprint.requirements[element]), self.robots),
                        inc_tuple(self.robots, element), self.blueprint, self.path + [element])
        else:
            return None

    def find_next(self) -> Iterator[Path]:
        if (path := self._check(Element.Geode)) is not None:
            yield path
        if self.blueprint.max_requirement(Element.Obsidian) >= self.material[Element.Obsidian]:
            if (path := self._check(Element.Obsidian)) is not None:
                yield path
        if self.blueprint.max_requirement(Element.Clay) >= self.material[Element.Clay]:
            if (path := self._check(Element.Clay)) is not None:
                yield path
        if self.blueprint.max_requirement(Element.Ore) >= self.material[Element.Ore]:
            if (path := self._check(Element.Ore)) is not None:
                yield path
        yield Path(self.time + 1, add(self.material, self.robots), self.robots, self.blueprint,
                   self.path + [None])

    def __lt__(self, other: Path) -> bool:
        if self.time != other.time:
            return self.time < other.time
        return self.material > other.material


@dataclass(slots=True)
class Blueprint:
    number: int
    requirements: tuple[Elements, Elements, Elements, Elements]

    @classmethod
    def create(cls, number: int, ore: int, clay: int,
               obsidian: tuple[int, int], geode: tuple[int, int]) -> Self:
        requirements = (
            (0, geode[1], 0, geode[0]),
            (0, 0, obsidian[1], obsidian[0]),
            (0, 0, 0, clay),
            (0, 0, 0, ore),
        )
        return Blueprint(number, requirements)

    @classmethod
    def parse(cls, line: str) -> Self:
        return blueprint_parser.parse(line).get()

    def max_requirement(self, element: Element) -> int:
        return round(max(requirement[element] for requirement in self.requirements) * 1.2)

    def run(self, rounds: int) -> int:
        queue: PriorityQueue[Path] = PriorityQueue()
        queue.put(Path.start(self))
        seen: dict[tuple[Elements, int], Elements] = {}
        while not queue.empty():
            current = queue.get()
            if ((current.robots, current.time) in seen
                    and gt(seen[(current.robots, current.time)], current.material)):
                continue
            seen[(current.robots, current.time)] = current.material

            if current.time == rounds:
                return current.material[Element.Geode]
            for next in current.find_next():
                queue.put(next)

        raise Exception("No optimum found")
