from __future__ import annotations

from typing import Iterator

day_num = 3


def part1(lines: Iterator[str]) -> int:
    return sum(Rucksack.find_double(line) for line in lines)


def part2(lines: Iterator[str]) -> int:
    groups = [lines] * 3
    zipped = zip(*groups, strict=True)
    return sum(Rucksack.find_common(group) for group in zipped)


class Rucksack:
    @staticmethod
    def priority(char: str) -> int:
        """
        Returns the priority given to each item.
        It is assumed, that we are given a valid item
        """
        num = ord(char)
        if ord('a') <= num and num <= ord('z'):
            return num - ord('a') + 1
        if ord('A') <= num and num <= ord('Z'):
            return num - ord('A') + 27
        raise Exception(f"Unknown char: {char}")

    @staticmethod
    def find_double(rucksack: str) -> int:
        """
        Finds the priority of the one item in both compartments.
        It is assumed that there is only one such item
        """
        half = len(rucksack) // 2
        first = rucksack[:half]
        second = rucksack[half:]
        for item in first:
            if item in second:
                return Rucksack.priority(item)
        raise Exception("No double item")

    @staticmethod
    def find_common(group: tuple[str, ...]) -> int:
        """
        Finds the one item in all three rucksacks given.
        It is assumed that there is only one such item and group has exactly three rucksacks
        """
        for item in group[0]:
            if item in group[1] and item in group[2]:
                return Rucksack.priority(item)
        raise Exception("No common item found")
