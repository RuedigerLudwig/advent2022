from advent.common import input

from .solution import day_num, part1, part2


def test_part1():
    data = input.read_lines(day_num, 'test01.txt')
    expected = 24_000
    result = part1(data)
    assert result == expected


def test_part2():
    data = input.read_lines(day_num, 'test01.txt')
    expected = 45_000
    result = part2(data)
    assert result == expected
