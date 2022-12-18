from advent.common import input

from .solution import day_num, marker, part1, part2


def test_part1():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 7
    result = part1(data)
    assert result == expected


def test_part2():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 19
    result = part2(data)
    assert result == expected


def test_marker04():
    input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    expected = 7
    result = marker(input, 4)
    assert result == expected


def test_marker14():
    input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    expected = 19
    result = marker(input, 14)
    assert result == expected
