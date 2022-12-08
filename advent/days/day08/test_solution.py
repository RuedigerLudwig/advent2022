from advent.common import utils

from .solution import Trees, day_num, part1, part2


def test_part1():
    data = utils.read_data(day_num, 'test01.txt')
    expected = 21
    result = part1(data)
    assert result == expected


def test_part2():
    data = utils.read_data(day_num, 'test01.txt')
    expected = 8
    result = part2(data)
    assert result == expected


def test_visible():
    data = utils.read_data(day_num, 'test01.txt')
    expected = 21
    result = Trees.parse(data).count_visible()
    assert result == expected


def test_distance():
    data = utils.read_data(day_num, 'test01.txt')
    expected = 4
    result = Trees.parse(data).single_scenic_score(2, 1)
    assert result == expected


def test_distance2():
    data = utils.read_data(day_num, 'test01.txt')
    expected = 8
    result = Trees.parse(data).single_scenic_score(2, 3)
    assert result == expected


def test_max_distance():
    data = utils.read_data(day_num, 'test01.txt')
    expected = 8
    result = Trees.parse(data).max_scenic_score()
    assert result == expected
