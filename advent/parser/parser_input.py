
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Protocol, Self

AllowedParserInput = str | Iterator[str]


def create_parser_input(input: AllowedParserInput) -> ParserInput:
    if isinstance(input, str):
        return SimpleParserInput(input, 0)
    else:
        return IteratorParserInput(StringDispenser(input), 0)


class ParserInput(Protocol):
    def step(self) -> tuple[Self, str]:
        ...

    def has_data(self) -> bool:
        ...


@dataclass(slots=True, frozen=True)
class SimpleParserInput:
    input: str
    start: int

    def step(self) -> tuple[Self, str]:
        if self.start >= len(self.input):
            raise Exception("Already at End of Input")

        return SimpleParserInput(self.input, self.start + 1), self.input[self.start]

    def has_data(self) -> bool:
        return self.start < len(self.input)

    def __repr__(self) -> str:
        if self.start == 0:
            return f'->[{self.input}]'
        if self.start >= len(self.input):
            return f'{self.input}'
        if self.start < 3:
            return f'{self.input[0:self.start-1]}->[{self.input[self.start:]}]'
        return f'{self.input[self.start-3:self.start-1]}->[{self.input[self.start:]}]'


@dataclass(slots=True)
class StringDispenser:
    lines: Iterator[str]
    input: str = field(default="", init=False)
    length: int = field(default=0, init=False)

    def read_more(self):
        try:
            part = next(self.lines)
            if self.input:
                self.input = f"{self.input}\n{part}"
            else:
                self.input = part
            self.length = len(self.input)
            return True
        except StopIteration:
            return False

    def get_str(self, pos: int) -> str | None:
        assert pos >= 0
        if pos < self.length:
            return self.input[pos]
        elif pos == self.length and pos != 0:
            return "\n"
        elif self.read_more():
            return self.get_str(pos)
        else:
            return None

    def has_more(self, pos: int) -> bool:
        assert pos >= 0
        if pos <= self.length:
            return True
        elif self.read_more():
            return self.has_more(pos)
        else:
            return False


@dataclass(slots=True, frozen=True)
class IteratorParserInput:
    dispenser: StringDispenser
    start: int

    def step(self) -> tuple[Self, str]:
        char = self.dispenser.get_str(self.start)
        if char is None:
            raise Exception("Already at End of Input")

        return IteratorParserInput(self.dispenser, self.start + 1), char

    def has_data(self) -> bool:
        return self.dispenser.has_more(self.start)
