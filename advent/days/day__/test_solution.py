from advent.common import utils

from .solution import day_num, part1, part2


def test_part1():
    data = utils.read_data(day_num, 'test01.txt')
    expected = None
    result = part1(data)
    assert result == expected


def test_part2():
    data = utils.read_data(day_num, 'test01.txt')
    expected = None
    result = part2(data)
    assert result == expected
