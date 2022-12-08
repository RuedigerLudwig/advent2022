from __future__ import annotations
from dataclasses import dataclass

from typing import Iterator

day_num = 8


def part1(lines: Iterator[str]) -> int:
    return Trees.parse(lines).count_visible()


def part2(lines: Iterator[str]) -> int:
    return Trees.parse(lines).max_scenic_score()


@dataclass(slots=True)
class Trees:
    trees: list[list[int]]
    width: int
    height: int

    @staticmethod
    def parse(lines: Iterator[str]) -> Trees:
        trees = [[int(tree) for tree in line] for line in lines]
        return Trees(trees, len(trees[0]), len(trees))

    def count_visible(self) -> int:
        visible = [[True] * self.width]
        for _ in range(self.height - 2):
            visible += [[True] + [False] * (self.width - 2) + [True]]
        visible += [[True] * self.width]

        # From Up
        mx = self.trees[0].copy()
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.trees[y][x] > mx[x]:
                    mx[x] = self.trees[y][x]
                    visible[y][x] = True

        # From Down
        mx = self.trees[-1].copy()
        for y in range(self.height - 2, 0, -1):
            for x in range(1, self.width - 1):
                if self.trees[y][x] > mx[x]:
                    mx[x] = self.trees[y][x]
                    visible[y][x] = True

        # From Left
        mx = [self.trees[y][0] for y in range(self.height)]
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if self.trees[y][x] > mx[y]:
                    mx[y] = self.trees[y][x]
                    visible[y][x] = True

        # From Right
        mx = [self.trees[y][-1] for y in range(self.height)]
        for x in range(self.width - 2, 0, -1):
            for y in range(1, self.height - 1):
                if self.trees[y][x] > mx[y]:
                    mx[y] = self.trees[y][x]
                    visible[y][x] = True

        return sum(1 for y in range(self.height) for x in range(self.width) if visible[y][x])

    def max_scenic_score(self) -> int:
        max_score = 0
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                score = self.single_scenic_score(x, y)
                if score > max_score:
                    max_score = score
        return max_score

    def single_scenic_score(self, x: int, y: int) -> int:
        up = 0
        for dy in range(y - 1, -1, -1):
            up += 1
            if self.trees[dy][x] >= self.trees[y][x]:
                break

        down = 0
        for dy in range(y + 1, self.height):
            down += 1
            if self.trees[dy][x] >= self.trees[y][x]:
                break

        left = 0
        for dx in range(x - 1, -1, -1):
            left += 1
            if self.trees[y][dx] >= self.trees[y][x]:
                break

        right = 0
        for dx in range(x + 1, self.width):
            right += 1
            if self.trees[y][dx] >= self.trees[y][x]:
                break

        return up * down * left * right
