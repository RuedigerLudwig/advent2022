from advent.common import input

from .solution import day_num, part1, part2


def test_part1():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 157
    result = part1(data)
    assert result == expected


def test_part2():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 70
    result = part2(data)
    assert result == expected
