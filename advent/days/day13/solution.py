from __future__ import annotations
from dataclasses import dataclass
from itertools import zip_longest

from typing import Iterator, Self

day_num = 13


def part1(lines: Iterator[str]) -> int:
    pairs = parse_all_pairs(lines)
    return sum(pos for pos, (left, right) in enumerate(pairs, start=1) if left < right)


def part2(lines: Iterator[str]) -> int:
    """ Why sort if your can simply count?"""
    marker2 = PacketList([[2]])
    marker6 = PacketList([[6]])

    p2 = 1
    p6 = 1
    for packet_list in (PacketList.parse(line) for line in lines if line):
        if packet_list < marker2:
            p2 += 1
        elif packet_list < marker6:
            p6 += 1

    return p2 * (p2 + p6)


ListOrInt = list["ListOrInt"] | int


@dataclass(slots=True, frozen=True, eq=False)
class PacketList:
    line: list[ListOrInt]

    @classmethod
    def _parse_sublist(cls, line_iter: Iterator[str]) -> list[ListOrInt]:
        """ Parses a sublist. Assumes that we do not find multiple commas, ot List in a row."""
        parsed: list[ListOrInt] = []
        number: int | None = None
        for character in line_iter:
            match character:
                case '[':
                    if number is not None:
                        raise Exception("Did not expect list")
                    parsed.append(cls._parse_sublist(line_iter))

                case ']':
                    if number is not None:
                        parsed.append(number)
                    return parsed

                case ',':
                    if number is not None:
                        parsed.append(number)
                        number = None

                case digit if digit.isdecimal():
                    if number is None:
                        number = int(digit)
                    else:
                        number = number * 10 + int(digit)

                case c:
                    raise Exception(f"Illegal Character: {c}")
        raise Exception("End of Input without reaching ']'")

    @classmethod
    def parse(cls, line: str) -> Self:
        """ Parses the given line into a PacktList """
        line_iter = iter(line)
        if next(line_iter) != '[':
            raise Exception(f"line does not start with [: {line}")

        return PacketList(cls._parse_sublist(line_iter))

    @classmethod
    def _comp_sublists(cls, left: list[ListOrInt], right: list[ListOrInt]) -> bool | None:
        """
        Compares two sublists.
        Return true if left comes before right
               false if right comes before left
               None if left and right are equal
        """
        for left_item, right_item in zip_longest(left, right, fillvalue=None):
            match (left_item, right_item):
                case int(left_int), int(right_int):
                    if left_int != right_int:
                        return left_int < right_int

                case list(left_list), list(right_list):
                    result = cls._comp_sublists(left_list, right_list)
                    if result is not None:
                        return result

                case int(left_int), list(right_list):
                    result = cls._comp_sublists([left_int], right_list)
                    if result is not None:
                        return result

                case list(left_list), int(right_int):
                    result = cls._comp_sublists(left_list, [right_int])
                    if result is not None:
                        return result

                case _:
                    return left_item is None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PacketList):
            return False
        return PacketList._comp_sublists(self.line, other.line) is None

    def __lt__(self, other: PacketList) -> bool:
        return PacketList._comp_sublists(self.line, other.line) is True


def parse_single_pair(lines: Iterator[str]) -> tuple[PacketList, PacketList]:
    return PacketList.parse(next(lines)), PacketList.parse(next(lines))


def parse_all_pairs(lines: Iterator[str]) -> list[tuple[PacketList, PacketList]]:
    result: list[tuple[PacketList, PacketList]] = []
    try:
        while True:
            result.append(parse_single_pair(lines))
            next(lines)
    except StopIteration:
        pass
    return result
