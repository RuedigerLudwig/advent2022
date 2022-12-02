from __future__ import annotations

from typing import Iterator
from enum import Enum

day_num = 2


def part1(lines: Iterator[str]) -> int:
    return sum(player.score(opponent) for opponent, player in (Shape.parse(line) for line in lines))


def part2(lines: Iterator[str]) -> int:
    return sum(result.score(opponent)
               for opponent, result in (Result.parse(line) for line in lines))


class Shape(Enum):
    """
    A class that prepresents the Shapes of Rock Paper Scissors.
    Rock beats Scissors
    Paper beats Rock
    Scissors beats Paper
    """
    Rock = 1
    Paper = 2
    Scissors = 3

    @staticmethod
    def parse(line: str) -> tuple[Shape, Shape]:
        """
        Parses a line into a game of RPC
        Parameters
        ----------
        line : str
            The line to be parsed

        Returns
        -------
        tuple[Shape, Shape]
            a tuple of the Shapes given. The first is the opponent, the second the player

        Raises
        ------
        Exception
            If either the line does not contain exactly two shapes,
            or either of the shapes is unknown
        """
        match line.strip().split():
            case [o, p]: return Shape.parse_opponent(o), Shape.parse_player(p)
            case _: raise Exception(f"Unknown line: {line}")

    @staticmethod
    def parse_opponent(char: str) -> Shape:
        """
        Parses a shape for RPC
        A -> Rock
        B -> Paper
        C -> Scissors
        Parameters
        ----------
        char : str
            The character to be parsed into a shape

        Returns
        -------
        Shape
            The shape described by the character

        Raises
        ------
        Exception
            If the character does not describe a valid shape
        """
        match char.strip().upper():
            case 'A': return Shape.Rock
            case 'B': return Shape.Paper
            case 'C': return Shape.Scissors
            case _: raise Exception(f"Unknown char : {char}")

    @staticmethod
    def parse_player(char: str) -> Shape:
        """
        Parses a shape for RPC using rules for player shapes
        X -> Rock
        Y -> Paper
        Z -> Scissors
        Parameters
        ----------
        char : str
            The character to be parsed into a shape

        Returns
        -------
        Shape
            The shape described by the character

        Raises
        ------
        Exception
            If the character does not describe a valid shape
        """
        match char.strip().upper():
            case 'X': return Shape.Rock
            case 'Y': return Shape.Paper
            case 'Z': return Shape.Scissors
            case _: raise Exception(f"Unknown char : {char}")

    def prev(self) -> Shape:
        """ The Shape preceding the curent one """
        return Shape((self.value + 1) % 3 + 1)

    def next(self) -> Shape:
        """ The Shape following the curent one """
        return Shape(self.value % 3 + 1)

    def beats(self, other: Shape) -> bool:
        """ true if this shape beats the other one """
        return self == other.next()

    def score(self, other: Shape) -> int:
        """ The score according to elf RPC rules """
        if self == other:
            points = 3
        elif self.beats(other):
            points = 6
        else:
            points = 0

        return self.value + points


class Result(Enum):
    Lose = 1
    Draw = 2
    Win = 3

    @staticmethod
    def parse(line: str) -> tuple[Shape, Result]:
        """
        Parses a line into a game of RPC with anm expected outcome
        Parameters
        ----------
        line : str
            The line to be parsed

        Returns
        -------
        tuple[Shape, Result]
            a tuple of the Shape the other play will use and an expected result

        Raises
        ------
        Exception
            If either the line does not contain exactly two items,
            or either the shape or result is unknown
        """
        match line.strip().split():
            case [o, r]: return Shape.parse_opponent(o), Result.parse_result(r)
            case _: raise Exception(f"Unknown line: {line}")

    @staticmethod
    def parse_result(char: str) -> Result:
        """
        Parses an expected result for RPC
        X -> Lose
        Y -> Draw
        Z -> Win
        Parameters
        ----------
        char : str
            The character to be parsed into a result

        Returns
        -------
        Result
            The result described by the character

        Raises
        ------
        Exception
            If the character does not describe a valid result
        """
        match char.strip().upper():
            case 'X': return Result.Lose
            case 'Y': return Result.Draw
            case 'Z': return Result.Win
            case _: raise Exception(f"Unknown char : {char}")

    def score(self, other: Shape) -> int:
        """ The score we get by the given shape and the expected result """
        match self:
            case Result.Lose: return other.prev().score(other)
            case Result.Draw: return other.score(other)
            case Result.Win: return other.next().score(other)
