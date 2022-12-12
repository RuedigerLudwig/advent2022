from advent.common import input

from .solution import Map, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 31
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 29
    result = part2(lines)
    assert result == expected


def test_path():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 31
    result = Map.create(lines).find_path('S')
    assert result == expected
