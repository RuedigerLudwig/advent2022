from advent.common import input

from .solution import day_num, part1, part2, from_snafu, to_snafu


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = "2=-1=0"
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = None
    result = part2(lines)
    assert result == expected


def test_976():
    input = "2=-01"
    expected = 976
    result = from_snafu(input)
    assert result == expected


def test_4890():
    input = 4890
    expected = "2=-1=0"
    result = to_snafu(input)
    assert result == expected
