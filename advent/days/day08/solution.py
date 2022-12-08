from __future__ import annotations
from dataclasses import dataclass

from typing import Iterator

day_num = 8


def part1(lines: Iterator[str]) -> int:
    return Forest.parse(lines).count_visible_trees()


def part2(lines: Iterator[str]) -> int:
    return Forest.parse(lines).max_scenic_score()


@dataclass(slots=True)
class Forest:
    trees: list[list[int]]
    width: int
    height: int

    @staticmethod
    def parse(lines: Iterator[str]) -> Forest:
        trees = [[int(tree) for tree in line] for line in lines]
        return Forest(trees, len(trees[0]), len(trees))

    def count_visible_trees(self) -> int:
        visible: set[tuple[int, int]] = set()

        # From Above
        mx = self.trees[0].copy()
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.trees[y][x] > mx[x]:
                    mx[x] = self.trees[y][x]
                    visible.add((x, y))

        # From Below
        mx = self.trees[-1].copy()
        for y in range(self.height - 2, 0, -1):
            for x in range(1, self.width - 1):
                if self.trees[y][x] > mx[x]:
                    mx[x] = self.trees[y][x]
                    visible.add((x, y))

        # From Left
        mx = [row[0] for row in self.trees]
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if self.trees[y][x] > mx[y]:
                    mx[y] = self.trees[y][x]
                    visible.add((x, y))

        # From Right
        mx = [row[-1] for row in self.trees]
        for x in range(self.width - 2, 0, -1):
            for y in range(1, self.height - 1):
                if self.trees[y][x] > mx[y]:
                    mx[y] = self.trees[y][x]
                    visible.add((x, y))

        return len(visible) + 2 * (self.width + self.height - 2)

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
