from advent.common import utils

from .solution import Command, day_num, part1, part2


def test_part1():
    data = utils.read_data(day_num, 'test01.txt')
    expected = 13
    result = part1(data)
    assert result == expected


def test_part2():
    data = utils.read_data(day_num, 'test02.txt')
    expected = 36
    result = part2(data)
    assert result == expected


def test_short():
    data = utils.read_data(day_num, 'test01.txt')
    expected = 13
    lst = [Command.parse(line) for line in data]
    result = Command.walk(lst, 2)
    assert result == expected


def test_long1():
    data = utils.read_data(day_num, 'test01.txt')
    expected = 1
    lst = [Command.parse(line) for line in data]
    result = Command.walk(lst, 10)
    assert result == expected


def test_long2():
    data = utils.read_data(day_num, 'test02.txt')
    expected = 36
    lst = [Command.parse(line) for line in data]
    result = Command.walk(lst, 10)
    assert result == expected
