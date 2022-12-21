from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

from typing import Iterator

day_num = 21


def part1(lines: Iterator[str]) -> int:
    troop = Monkey.parse_troop(lines)
    return troop["root"].get_value(troop)


def part2(lines: Iterator[str]) -> int:
    troop = Monkey.parse_troop(lines)

    root = troop["root"]
    new_root = Monkey("root", None, Operation.Sub, root.monkeys)

    result = new_root.reach_value(0, troop, 'humn')
    if result is None:
        raise Exception("Can't find solution")

    return result


class Operation(Enum):
    Add = 0
    Sub = 1
    Mul = 2
    Div = 3

    def calc_value(self, value1: int, value2: int) -> int:
        match self:
            case Operation.Add: return value1 + value2
            case Operation.Sub: return value1 - value2
            case Operation.Mul: return value1 * value2
            case Operation.Div: return value1 // value2

    def calc_value1(self, value: int, value2: int) -> int:
        match self:
            case Operation.Add: return value - value2
            case Operation.Sub: return value + value2
            case Operation.Mul: return value // value2
            case Operation.Div: return value * value2

    def calc_value2(self, value: int, value1: int) -> int:
        match self:
            case Operation.Add: return value - value1
            case Operation.Sub: return value1 - value
            case Operation.Mul: return value // value1
            case Operation.Div: return value1 // value


@dataclass(slots=True, frozen=True)
class Monkey:
    name: str
    value: int | None

    operation: Operation | None = field(default=None)
    monkeys: tuple[str, str] | None = field(default=None)

    @classmethod
    def parse_troop(cls, lines: Iterator[str]) -> dict[str, Monkey]:
        troop = {monkey.name: monkey for monkey in (Monkey.parse(line) for line in lines)}
        return troop

    @classmethod
    def parse(cls, line: str) -> Monkey:
        match line.split(': '):
            case [name, formula]:
                match formula.split():
                    case [value]:
                        return Monkey(name, int(value))

                    case [monkey1, '+', monkey2]:
                        return Monkey(name, None, Operation.Add, (monkey1, monkey2))
                    case [monkey1, '-', monkey2]:
                        return Monkey(name, None, Operation.Sub, (monkey1, monkey2))
                    case [monkey1, '*', monkey2]:
                        return Monkey(name, None, Operation.Mul, (monkey1, monkey2))
                    case [monkey1, '/', monkey2]:
                        return Monkey(name, None, Operation.Div, (monkey1, monkey2))

                    case _:
                        raise Exception(f"Unknown formula: {formula}")
            case _:
                raise Exception(f"Unknown line: {line}")

    def get_value(self, troop: dict[str, Monkey]) -> int:
        if self.value is not None:
            return self.value

        if self.monkeys is None or self.operation is None:
            raise Exception("Illegal state")

        value1 = troop[self.monkeys[0]].get_value(troop)
        value2 = troop[self.monkeys[1]].get_value(troop)

        return self.operation.calc_value(value1, value2)

    def get_for_human(self, troop: dict[str, Monkey], human_name: str) -> int | None:
        if self.name == human_name:
            return None

        if self.value is not None:
            return self.value

        if self.monkeys is None or self.operation is None:
            raise Exception("Illegal state")

        value1 = troop[self.monkeys[0]] .get_for_human(troop, human_name)
        value2 = troop[self.monkeys[1]] .get_for_human(troop, human_name)

        if value1 is None or value2 is None:
            return None

        return self.operation.calc_value(value1, value2)

    def reach_value(self, value: int, troop: dict[str, Monkey], human_name: str) -> int:
        if self.name == human_name:
            return value

        if self.monkeys is None or self.operation is None:
            raise Exception("Illegal state")

        monkey1 = troop[self.monkeys[0]]
        monkey2 = troop[self.monkeys[1]]

        value1 = monkey1.get_for_human(troop, human_name)
        value2 = monkey2.get_for_human(troop, human_name)

        assert value1 is None or value2 is None

        if value1 is not None:
            value2 = self.operation.calc_value2(value, value1)
            return monkey2.reach_value(value2, troop, human_name)

        elif value2 is not None:
            value1 = self.operation.calc_value1(value, value2)
            return monkey1.reach_value(value1, troop, human_name)

        assert False, "Unreachable"
