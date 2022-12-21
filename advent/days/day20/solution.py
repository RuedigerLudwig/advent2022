from __future__ import annotations
from dataclasses import dataclass

from typing import Iterable, Iterator, Self

day_num = 20


def part1(lines: Iterator[str]) -> int:
    ring = Ring.create(int(line) for line in lines)
    ring.process(1)
    return sum(ring.get_ordered([1000, 2000, 3000]))


def part2(lines: Iterator[str]) -> int:
    ring = Ring.create(int(line) * 811589153 for line in lines)
    ring.process(10)
    return sum(ring.get_ordered([1000, 2000, 3000]))


@dataclass(slots=True)
class Ring:
    """ Datastructure that stores Items in a Ring """
    items: list[RingItem]

    @classmethod
    def create(cls, values: Iterable[int]):
        """ Crates ring from an Iterable """
        value_iterator = iter(values)

        current = RingItem.create(next(value_iterator))
        items = [current]
        for value in value_iterator:
            current = current.append(value)
            items.append(current)

        return Ring(items)

    @property
    def zero(self) -> RingItem:
        """ Helper to find the first item with value zero. Raises Exception if there is none. """
        for item in self.items:
            if item.value == 0:
                return item
        raise Exception("No Zero Item found")

    def process(self, rounds: int):
        """ Processes the given number of complete rounds. """
        for _ in range(rounds):
            for item in self.items:
                item.move(len(self.items))

    def get_ordered(self, values: list[int]) -> Iterator[int]:
        """ Returns the values at the given ordered positions """
        for n, item in zip(range(max(values) + 1), self.zero):
            if n in values:
                yield item


@dataclass(slots=True)
class RingItem:
    """ A class to store one Item in a Ring"""
    value: int
    next: RingItem
    prev: RingItem

    @classmethod
    def create(cls, value: int) -> Self:
        """ Creates a single Ring Element that points to itself"""
        root = RingItem(value, None, None)  # type: ignore
        root.next = root
        root.prev = root
        return root

    def append(self, value: int) -> RingItem:
        """ Appends the given value to the current element """
        next = RingItem(value, self.next, self)
        self.next.prev = next
        self.next = next
        return next

    def move(self, item_count: int):
        """  Moves the current element according to its value """
        steps = self.value % (item_count - 1)

        if steps == 0:
            return

        self.next.prev = self.prev
        self.prev.next = self.next

        new_pos = self
        for _ in range(steps):
            new_pos = new_pos.next

        self.prev = new_pos
        self.next = new_pos.next

        new_pos.next.prev = self
        new_pos.next = self

    def __iter__(self) -> Iterator[int]:
        """ Never ending iterator through items"""
        current = self
        while True:
            yield current.value
            current = current.next

    def stopping(self) -> Iterator[int]:
        """ Iterator that iterates exactly once through all items """
        current = self
        while True:
            yield current.value
            current = current.next
            if current == self:
                break
