from __future__ import annotations

from typing import Iterator

day_num = 3


def part1(lines: Iterator[str]) -> int:
    return sum(priority(find_double(line)) for line in lines)


def part2(lines: Iterator[str]) -> int:
    groups = zip(lines, lines, lines, strict=True)
    return sum(priority(find_common_item(group)) for group in groups)


def priority(char: str) -> int:
    """
    Returns the priority given to each item.
    It is assumed, that we are given a valid item
    """
    if 'a' <= char and char <= 'z':
        return ord(char) - ord('a') + 1
    if 'A' <= char and char <= 'Z':
        return ord(char) - ord('A') + 27
    raise Exception(f"Unknown char: {char}")


def find_double(rucksack: str) -> str:
    """
    Finds the one item in both compartments.
    It is assumed that there is only one such item
    """
    half = len(rucksack) // 2
    first = rucksack[:half]
    second = rucksack[half:]
    for item in first:
        if item in second:
            return item
    raise Exception("No double item")


def find_common_item(group: tuple[str, str, str]) -> str:
    """
    Finds the one item in all three rucksacks given.
    It is assumed that there is only one such item and group has exactly three rucksacks
    """
    first, second, third = group
    for item in first:
        if item in second and item in third:
            return item
    raise Exception("No common item found")
