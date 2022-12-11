from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from math import prod

from typing import Callable, Iterator, Self
from advent.parser.parser import P

day_num = 11


def part1(lines: Iterator[str]) -> int:
    horde = Troop_While_Worried.parse(lines)
    horde.rounds(20)
    return horde.inspected_result()


def part2(lines: Iterator[str]) -> int:
    horde = Troop_While_Kinda_Relieved.parse(lines)
    horde.rounds(10_000)
    return horde.inspected_result()


def worry_increaser(op: str, value: int | str) -> WorryIncreaser:
    match (op, value):
        case '*', int(v): return lambda old: old * v
        case '*', 'old': return lambda old: old ** 2
        case '+', int(v): return lambda old: old + v
        case '+', 'old': return lambda old: 2 * old
        case _: raise Exception(f"Illegal line: {op} {value}")


class Parser:
    """ All the parsers needed for this solution """
    worry_inc: P[WorryIncreaser] = P.second(
        P.tstring("Operation: new = old"),
        P.map2(P.one_of('+*'), P.either(P.tstring('old'), P.tsigned()),
               worry_increaser)).tline()
    monkey_number: P[int] = P.unsigned().between(P.tstring('Monkey'), P.tchar(':')).tline()
    items: P[list[int]] = P.second(
        P.tstring('Starting items:'), P.unsigned().sep_by(sep=P.tchar(','))).tline()
    modulo: P[int] = P.second(
        P.tstring("Test: divisible by"), P.unsigned()).tline()
    throw_parser: P[int] = P.second(
        P.seq(
            P.tstring("If"),
            P.either(P.tstring("true"), P.tstring("false")),
            P.tstring(": throw to monkey")),
        P.unsigned()).tline()
    test: P[tuple[int, int, int]] = P.seq(
        modulo, throw_parser, throw_parser)
    monkey: P[Monkey] = P.map4(monkey_number, items,
                               worry_inc, test,
                               lambda number, items, worry_inc, test:
                               Monkey(number, items, worry_inc, *test))
    monkey_list: P[list[Monkey]] = P.first(monkey, P.eol().optional()).many()


WorryIncreaser = Callable[[int], int]


@dataclass(slots=True)
class Monkey:
    number: int
    items: list[int]
    worry_increaser: WorryIncreaser
    modulator: int
    target_if_divides: int
    catcher_if_not_divides: int
    inspected: int = field(default=0, compare=False)

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
    """ The """
    @classmethod
    def parse(cls, lines: Iterator[str]) -> Self:
        monkeys = Parser.monkey_list.parse_iterator(lines).get()
        return Troop_While_Worried(monkeys)

    def single_round(self):
        for currentMonkey in self.monkeys:
            for target_monkey, item in currentMonkey.inspect_items(3):
                self.monkeys[target_monkey].catch_item(item)


@dataclass(slots=True)
class Troop_While_Kinda_Relieved(Troop):
    modulator: int

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Self:
        monkeys = Parser.monkey_list.parse_iterator(lines).get()
        return Troop_While_Kinda_Relieved(monkeys, prod(monkey.modulator for monkey in monkeys))

    def single_round(self):
        for current_monkey in self.monkeys:
            for target_monkey, item in current_monkey.inspect_items(None):
                self.monkeys[target_monkey].catch_item(item % self.modulator)
