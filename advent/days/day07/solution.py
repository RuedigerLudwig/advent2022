from __future__ import annotations
from dataclasses import dataclass, field

from typing import Iterator

day_num = 7


def part1(lines: Iterator[str]) -> int:
    return Directory.parse(lines).get_maxed_size(100_000)


def part2(lines: Iterator[str]) -> int:
    directory = Directory.parse(lines)
    return directory.get_min_delete_size(70_000_000, 30_000_000)


@dataclass(slots=True)
class Directory:
    name: str
    parent: Directory | None
    subdirs: list[Directory] = field(default_factory=list)
    files: list[tuple[str, int]] = field(default_factory=list)
    size: int | None = None

    def cd_into(self, name: str) -> Directory:
        """
        Returns the named sub directory or .. for parent
        May fail if unkown subdirectory - or already in root
        """
        if name == "..":
            if self.parent is None:
                raise Exception('Already at root Directory')
            return self.parent

        for sub in self.subdirs:
            if sub.name == name:
                return sub
        raise Exception(f"Could not find subdir {name}")

    def add_directory(self, name: str):
        """ Adds the named directory."""
        self.subdirs.append(Directory(name, self))

    def add_file(self, name: str, size: int):
        """ Adds the given file and size """
        self.files.append((name, size))

    def get_size(self) -> int:
        """ returns the size of this directory including all subdirectories """
        if self.size is None:
            self.size = (sum(size for _, size in self.files)
                         + sum(sub.get_size() for sub in self.subdirs))
        return self.size

    def get_all_directories(self) -> Iterator[Directory]:
        """ Returns an iterator of all subdirectories """
        for sub in self.subdirs:
            yield from sub.get_all_directories()
        yield self

    def get_maxed_size(self, threshold: int) -> int:
        """ Returns the sum of all sizes of subdirectories, that are below the given threshold"""
        return sum(size for size in
                   (dir.get_size() for dir in self.get_all_directories())
                   if size <= threshold)

    def get_min_delete_size(self, disk_size: int, space_needed: int) -> int:
        """
        Returns the size of the smallest directory that must be removed to created the free space
        given as a parameter and the given disk size
        #"""
        unused = disk_size - self.get_size()
        minimum: int | None = None
        for dir in self.get_all_directories():
            size = dir.get_size()
            if unused + size >= space_needed and (minimum is None or minimum > size):
                minimum = size

        if minimum is None:
            raise Exception("Could not find large enough directory to remove")

        return minimum

    @staticmethod
    def parse(lines: Iterator[str]) -> Directory:
        line = next(lines)
        if line != '$ cd /':
            raise Exception(f"Illegal first line: {line}")

        root = Directory('/', None)
        current = root
        for line in lines:
            match line.split():
                case ['$', 'cd', name]:
                    current = current.cd_into(name)

                case ['$', 'ls']:
                    pass

                case ['dir', name]:
                    current.add_directory(name)

                case [size, name]:
                    current.add_file(name, int(size))

                case _:
                    raise Exception(f"Could not parse line: {line}")

        return root
