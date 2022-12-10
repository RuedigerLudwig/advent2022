from __future__ import annotations
from dataclasses import dataclass

from typing import ClassVar, Iterator, Self

from advent.parser.parser import P

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

    amount_parser: ClassVar[P[int]] = P.second(P.string("move "), P.unsigned())
    from_parser: ClassVar[P[int]] = P.second(P.string(" from "), P.unsigned())
    to_parser: ClassVar[P[int]] = P.second(P.string(" to "), P.unsigned())
    move_parser: ClassVar[P[tuple[int, int, int]]] = P.seq(amount_parser, from_parser, to_parser)

    @classmethod
    def parse(cls, line: str) -> Self | None:
        parsed = cls.move_parser.parse(line)
        if parsed.is_fail():
            return None
        amount, frm, to = parsed.get()
        return cls(amount, frm - 1, to - 1)

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

    crate_parser: ClassVar[P[str | None]] = P.either(
        P.one_char().in_brackets(), P.string("   ").replace(None))
    crate_row_parser: ClassVar[P[list[str | None]]] = crate_parser.sep_by(P.is_char(' '))

    @classmethod
    def parse_crate_row(cls, line: str) -> list[None | str] | None:
        return Crane.crate_row_parser.parse(line).get_or(None)

    @classmethod
    def parse_stacks(cls, lines: Iterator[str]) -> list[str]:
        stacks: list[str] = []
        for line in lines:
            crate_row = Crane.parse_crate_row(line)
            if crate_row is None:
                return stacks

            if len(stacks) < len(crate_row):
                stacks += [""] * (len(crate_row) - len(stacks))

            for stack_num, crate in enumerate(crate_row):
                if crate is not None:
                    stacks[stack_num] = crate + stacks[stack_num]

        raise Exception("Can never happen")

    @classmethod
    def parse(cls, lines: Iterator[str], is_9001: bool) -> Self:
        drawing = cls.parse_stacks(lines)
        moves = [p for p in (Move.parse(line) for line in lines) if p is not None]
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
