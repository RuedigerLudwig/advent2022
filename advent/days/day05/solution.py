from __future__ import annotations
from dataclasses import dataclass

from typing import Iterator, Self

day_num = 5


def part1(lines: Iterator[str]) -> str:
    crane = Crane.parse(lines, False)
    crates = crane.perform_all_moves()
    return Crane.top(crates)


def part2(lines: Iterator[str]) -> str:
    crane = Crane.parse(lines, True)
    crates = crane.perform_all_moves()
    return Crane.top(crates)


@dataclass(slots=True, frozen=True)
class Move:
    amount: int
    frm: int
    to: int

    @classmethod
    def parse(cls, line: str) -> Self:
        match line.split():
            case ['move', amount, 'from', frm, 'to', to]:
                return cls(int(amount), int(frm) - 1, int(to) - 1)
            case _:
                raise Exception("Not a valid move")

    def do_move(self, crates: list[str], as_9001: bool) -> list[str]:
        """
        Moves the given crates by the provided move. Will fail if there are not enough crates
        in the stack to take crates off
        """
        if as_9001:
            crates[self.to] += crates[self.frm][-self.amount:]
        else:
            crates[self.to] += crates[self.frm][-self.amount:][::-1]
        crates[self.frm] = crates[self.frm][:-self.amount]
        return crates


@dataclass(slots=True, frozen=True)
class Crane:
    stacks: list[str]
    moves: list[Move]
    is_9001: bool

    @classmethod
    def parse_crate_row(cls, line: str) -> list[None | str]:
        result: list[str | None] = []
        for c in line[1::4]:
            if c.isalnum():
                result.append(c)
            else:
                result.append(None)
        return result

    @classmethod
    def parse_stacks(cls, lines: Iterator[str]) -> list[str]:
        stacks: list[str] = []
        for line in lines:
            if not line:
                return stacks
            crate_row = Crane.parse_crate_row(line)

            if len(stacks) < len(crate_row):
                stacks += [""] * (len(crate_row) - len(stacks))

            for stack_num, crate in enumerate(crate_row):
                if crate is not None:
                    stacks[stack_num] = crate + stacks[stack_num]

        raise Exception("Can never happen")

    @classmethod
    def parse(cls, lines: Iterator[str], is_9001: bool) -> Self:
        drawing = cls.parse_stacks(lines)
        moves = [Move.parse(line) for line in lines]
        return cls(drawing, moves, is_9001)

    @classmethod
    def top(cls, crates: list[str]) -> str:
        """ Lists the last item in the given stacks. Fails if any stack is empty """
        return ''.join(stack[-1] for stack in crates)

    def perform_all_moves(self) -> list[str]:
        stacks = self.stacks
        for move in self.moves:
            stacks = move.do_move(stacks, self.is_9001)
        return stacks
