from __future__ import annotations
from dataclasses import dataclass

from typing import Iterator

from advent.parser.parser import P

day_num = 5


def part1(lines: Iterator[str]) -> str:
    state = State.parse(lines)
    crates = state.all_moves9000()
    return State.top(crates)


def part2(lines: Iterator[str]) -> str:
    state = State.parse(lines)
    crates = state.all_moves9001()
    return State.top(crates)


crate_parser: P[str | None] = P.either(P.any_char().in_brackets(), P.string("   ").replace(None))
crate_row_parser = crate_parser.sep_by(P.is_char(' '))
amount_parser = P.snd(P.string("move "), P.unsigned())
from_parser = P.snd(P.string(" from "), P.unsigned())
to_parser = P.snd(P.string(" to "), P.unsigned())
move_parser = P.seq(amount_parser, from_parser, to_parser)


@dataclass(slots=True)
class State:
    crates: list[str]
    moves: list[tuple[int, int, int]]

    @staticmethod
    def parse_crate_line(line: str) -> list[None | str] | None:
        return crate_row_parser.parse(line).get_or(None)

    @staticmethod
    def parse_drawing(lines: Iterator[str]) -> list[str]:
        result: list[str] = []
        for line in lines:
            crates = State.parse_crate_line(line)
            if crates is None:
                return result

            if len(result) < len(crates):
                result += [""] * (len(crates) - len(result))
            for stack, crate in enumerate(crates):
                if crate is not None:
                    result[stack] = crate + result[stack]

        raise Exception("Can never happen")

    @staticmethod
    def parse_move(line: str) -> tuple[int, int, int]:
        amount, frm, to = move_parser.parse(line).get()
        return amount, frm - 1, to - 1

    @staticmethod
    def parse(lines: Iterator[str]) -> State:
        drawing = State.parse_drawing(lines)
        next(lines)
        moves = [State.parse_move(line) for line in lines]
        return State(drawing, moves)

    @staticmethod
    def do_move9000(crates: list[str], move: tuple[int, int, int]) -> list[str]:
        """
        Moves the given crates by the provided move. Will fail if there are not enough crates
        in the from stack
        """
        for _ in range(move[0]):
            crates[move[2]] += crates[move[1]][-1]
            crates[move[1]] = crates[move[1]][:-1]

        return crates

    def all_moves9000(self) -> list[str]:
        crates = self.crates
        for move in self.moves:
            crates = State.do_move9000(crates, move)
        return crates

    @staticmethod
    def do_move9001(crates: list[str], move: tuple[int, int, int]) -> list[str]:
        """
        Moves the given crates by the provided move. Will fail if there are not enough crates
        in the from stack
        """
        crates[move[2]] += crates[move[1]][-move[0]:]
        crates[move[1]] = crates[move[1]][:-move[0]]
        return crates

    def all_moves9001(self) -> list[str]:
        crates = self.crates
        for move in self.moves:
            crates = State.do_move9001(crates, move)
        return crates

    @staticmethod
    def top(crates: list[str]) -> str:
        """ Lists the last item in the given stacks. Fails if any stack is empty """
        return ''.join(stack[-1] for stack in crates)
