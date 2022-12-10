from pathlib import Path, PurePath
from typing import Iterator, TypeVar

T = TypeVar('T')


def read_lines(day: int, file_name: str) -> Iterator[str]:
    '''
    Returns an iterator over the content of the mentioned file
    All lines are striped of an eventual trailing '\n' their
    '''
    with open(
        Path.cwd()
        / PurePath('advent/days/day{0:02}/data'.format(day))
        / PurePath(file_name),
        'rt',
    ) as file:
        while line := file.readline():
            yield line.rstrip('\n')
