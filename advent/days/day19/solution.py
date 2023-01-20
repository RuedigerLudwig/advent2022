from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from itertools import islice
from math import prod
from multiprocessing import Pool
from queue import PriorityQueue
import re
from typing import Iterable, Iterator, Self


day_num = 19


def part1(lines: Iterator[str]) -> int:
    return sum(bp.number * geodes for bp, geodes in Processor.pool_it(24, lines))


def part2(lines: Iterator[str]) -> int:
    return prod(num for _, num in Processor.pool_it(32, islice(lines, 3)))


@dataclass(slots=True, frozen=True)
class Processor:
    rounds: int

    @classmethod
    def pool_it(cls, rounds: int, lines: Iterator[str]) -> Iterable[tuple[Blueprint, int]]:
        with Pool() as p:
            return p.map(Processor(rounds), lines)

    def __call__(self, line: str) -> tuple[Blueprint, int]:
        blueprint = Blueprint.parse(line)
        return blueprint, blueprint.run(self.rounds)


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


def inc_element(elements: Elements, pos: Element) -> Elements:
    return tuple(v + 1 if num == pos else v for num, v in enumerate(elements))


MAGIC_MATERIAL_SURPLUS = 1.2


@dataclass(slots=True)
class State:
    time: int
    material: Elements
    robots: Elements
    blueprint: Blueprint

    @classmethod
    def start(cls, blueprint: Blueprint) -> State:
        return State(0, (0, 0, 0, 0), (0, 0, 0, 1), blueprint)

    def get_valid_production(self, element: Element) -> State | None:
        if element != Element.Geode:
            max_needed = self.blueprint.max_needed[element]
            if self.robots[element] >= max_needed:
                return None
            if self.material[element] > round(max_needed * MAGIC_MATERIAL_SURPLUS):
                return None

        if gt(self.material, self.blueprint.requirements[element]):
            return State(self.time + 1,
                         add(sub(self.material, self.blueprint.requirements[element]), self.robots),
                         inc_element(self.robots, element), self.blueprint)
        else:
            return None

    def find_next(self) -> Iterator[State]:
        for element in Element:
            if (path := self.get_valid_production(element)) is not None:
                yield path

        yield State(self.time + 1, add(self.material, self.robots), self.robots, self.blueprint)

    def __lt__(self, other: State) -> bool:
        if self.time != other.time:
            return self.time < other.time
        return self.material > other.material


r_number = r"Blueprint (?P<number>\d+):"
r_ore = r".*(?P<ore_ore>\d+) ore."
r_clay = r".*(?P<clay_ore>\d+) ore."
r_obsidian = r".*(?P<obsidian_ore>\d+) ore and (?P<obsidian_clay>\d+) clay."
r_geode = r".*(?P<geode_ore>\d+) ore and (?P<geode_obsidian>\d+) obsidian."

pattern = re.compile(r_number + r_ore + r_clay + r_obsidian + r_geode)


@dataclass(slots=True)
class Blueprint:
    number: int
    requirements: tuple[Elements, Elements, Elements, Elements]
    max_needed: Elements

    @classmethod
    def create(cls, number: int, ore: int, clay: int,
               obsidian: tuple[int, int], geode: tuple[int, int]) -> Self:
        requirements = (
            (0, geode[1], 0, geode[0]),
            (0, 0, obsidian[1], obsidian[0]),
            (0, 0, 0, clay),
            (0, 0, 0, ore),
        )
        max_needed = (0, geode[1], obsidian[1], max(geode[0], obsidian[0], clay, ore))
        return Blueprint(number, requirements, max_needed)

    @classmethod
    def parse(cls, line: str) -> Self:
        result = pattern.match(line)
        if result is None:
            raise Exception("Not a valid Blueprint")
        return Blueprint.create(
            number=int(result.group('number')),
            ore=int(result.group('ore_ore')),
            clay=int(result.group('clay_ore')),
            obsidian=(int(result.group('obsidian_ore')), int(result.group('obsidian_clay'))),
            geode=(int(result.group('geode_ore')), int(result.group('geode_obsidian'))),
        )

    def run(self, rounds: int) -> int:
        queue: PriorityQueue[State] = PriorityQueue()
        queue.put(State.start(self))
        seen: dict[tuple[Elements, int], Elements] = {}
        while not queue.empty():
            current = queue.get()
            last_seen = seen.get((current.robots, current.time))
            if last_seen is not None and gt(last_seen, current.material):
                continue
            seen[(current.robots, current.time)] = current.material

            if current.time == rounds:
                return current.material[Element.Geode]
            for next in current.find_next():
                queue.put(next)

        raise Exception("No optimum found")
