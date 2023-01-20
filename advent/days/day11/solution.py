from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from math import prod
import re

from typing import Callable, Iterator, Self

day_num = 11


def part1(lines: Iterator[str]) -> int:
    horde = Troop_While_Worried.parse(lines)
    horde.rounds(20)
    return horde.inspected_result()


def part2(lines: Iterator[str]) -> int:
    horde = Troop_While_Kinda_Relieved.parse(lines)
    horde.rounds(10_000)
    return horde.inspected_result()


WorryIncreaser = Callable[[int], int]


def match_raise(pattern: str, string: str) -> re.Match[str]:
    result = re.match(pattern, string)
    if result is None:
        raise Exception("Pattern did not match")
    return result


@dataclass(slots=True)
class Monkey:
    number: int
    items: list[int]
    worry_increaser: WorryIncreaser
    modulator: int
    target_if_divides: int
    catcher_if_not_divides: int
    inspected: int = field(default=0, compare=False)

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Monkey:
        re_number = match_raise(r"Monkey (?P<number>\d+):", next(lines))
        number = int(re_number.group('number'))
        starting = next(lines).split(":")
        items = list(int(item.strip()) for item in starting[1].split(","))
        s_operation = next(lines).split('=')
        match s_operation[1].split():
            case ['old', '*', 'old']:
                operation: WorryIncreaser = lambda old: old ** 2
            case ['old', '*', num]:
                number = int(num)
                operation: WorryIncreaser = lambda old: old * number
            case ['old', '+', num]:
                number = int(num)
                operation: WorryIncreaser = lambda old: old + number
            case _: raise Exception("Illegal operation")
        s_modulo = next(lines).split("by")
        modulo = int(s_modulo[1].strip())
        s_if_true = next(lines).split("monkey")
        if_true = int(s_if_true[1])
        s_if_false = next(lines).split("monkey")
        if_false = int(s_if_false[1])
        return Monkey(number, items, operation, modulo, if_true, if_false)

    def inspect_items(self, worry_decrease: int | None) -> Iterator[tuple[int, int]]:
        for item in self.items:
            self.inspected += 1
            next_level = self.worry_increaser(item)

            if worry_decrease is not None:
                next_level //= worry_decrease

            if next_level % self.modulator == 0:
                target_monkey = self.target_if_divides
            else:
                target_monkey = self.catcher_if_not_divides

            yield target_monkey, next_level
        self.items.clear()

    def catch_item(self, item: int):
        self.items.append(item)


@dataclass(slots=True)
class Troop(ABC):
    monkeys: list[Monkey]

    @classmethod
    def parse_monkeys(cls, lines: Iterator[str]) -> Iterator[Monkey]:
        while True:
            try:
                yield Monkey.parse(lines)
                next(lines)
            except StopIteration:
                return

    @abstractmethod
    def single_round(self):
        ...

    def rounds(self, count: int):
        for _ in range(count):
            self.single_round()

    def inspected_result(self):
        most = sorted((monkey.inspected for monkey in self.monkeys), reverse=True)
        return most[0] * most[1]


@dataclass(slots=True)
class Troop_While_Worried(Troop):
    @classmethod
    def parse(cls, lines: Iterator[str]) -> Self:
        return Troop_While_Worried(list(Troop.parse_monkeys(lines)))

    def single_round(self):
        for currentMonkey in self.monkeys:
            for target_monkey, item in currentMonkey.inspect_items(3):
                self.monkeys[target_monkey].catch_item(item)


@dataclass(slots=True)
class Troop_While_Kinda_Relieved(Troop):
    modulator: int

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Self:
        monkeys = list(Troop.parse_monkeys(lines))
        return Troop_While_Kinda_Relieved(monkeys, prod(monkey.modulator for monkey in monkeys))

    def single_round(self):
        for current_monkey in self.monkeys:
            for target_monkey, item in current_monkey.inspect_items(None):
                self.monkeys[target_monkey].catch_item(item % self.modulator)
