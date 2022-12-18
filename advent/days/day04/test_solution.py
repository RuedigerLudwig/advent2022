from advent.common import input

from .solution import Pair, Range, day_num, part1, part2


def test_part1():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 2
    result = part1(data)
    assert result == expected


def test_part2():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 4
    result = part2(data)
    assert result == expected


def test_parse():
    input = "2-4,6-8"
    expected = Pair(Range(2, 4), Range(6, 8))
    result = Pair.parse(input)
    assert result == expected
