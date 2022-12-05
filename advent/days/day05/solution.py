from __future__ import annotations
from dataclasses import dataclass

from typing import ClassVar, Iterator

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

    amount_parser: ClassVar[P[int]] = P.snd(P.string("move "), P.unsigned())
    from_parser: ClassVar[P[int]] = P.snd(P.string(" from "), P.unsigned())
    to_parser: ClassVar[P[int]] = P.snd(P.string(" to "), P.unsigned())
    move_parser: ClassVar[P[tuple[int, int, int]]] = P.seq(amount_parser, from_parser, to_parser)

    @staticmethod
    def parse(line: str) -> Move:
        amount, frm, to = Move.move_parser.parse(line).get()
        return Move(amount, frm - 1, to - 1)

    def do_move(self, crates: list[str], as_9001: bool) -> list[str]:
        """
        Moves the given crates by the provided move. Will fail if there are not enough crates
        in the from stack
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
        P.any_char().in_brackets(), P.string("   ").replace(None))
    crate_row_parser: ClassVar[P[list[str | None]]] = crate_parser.sep_by(P.is_char(' '))

    @staticmethod
    def parse_crate_row(line: str) -> list[None | str] | None:
        return Crane.crate_row_parser.parse(line).get_or(None)

    @staticmethod
    def parse_drawing(lines: Iterator[str]) -> list[str]:
        stacks: list[str] = []
        for line in lines:
            crate_row = Crane.parse_crate_row(line)
            if crate_row is None:
                next(lines)  # Empty line
                return stacks

            if len(stacks) < len(crate_row):
                stacks += [""] * (len(crate_row) - len(stacks))

            for stack_num, crate in enumerate(crate_row):
                if crate is not None:
                    stacks[stack_num] = crate + stacks[stack_num]

        raise Exception("Can never happen")

    @staticmethod
    def parse(lines: Iterator[str], is_9001: bool) -> Crane:
        drawing = Crane.parse_drawing(lines)
        moves = [Move.parse(line) for line in lines]
        return Crane(drawing, moves, is_9001)

    @staticmethod
    def top(crates: list[str]) -> str:
        """ Lists the last item in the given stacks. Fails if any stack is empty """
        return ''.join(stack[-1] for stack in crates)

    def perform_all_moves(self) -> list[str]:
        stacks = self.stacks
        for move in self.moves:
            stacks = move.do_move(stacks, self.is_9001)
        return stacks
