from advent.common import input

from .solution import Command, day_num, part1, part2, simulate


def test_part1():
    data = input.read_lines(day_num, 'test01.txt')
    expected = 13
    result = part1(data)
    assert result == expected


def test_part2():
    data = input.read_lines(day_num, 'test02.txt')
    expected = 36
    result = part2(data)
    assert result == expected


def test_short():
    data = input.read_lines(day_num, 'test01.txt')
    expected = 13
    lst = (Command.parse(line) for line in data)
    result = simulate(lst, 2)
    assert result == expected


def test_long1():
    data = input.read_lines(day_num, 'test01.txt')
    expected = 1
    lst = (Command.parse(line) for line in data)
    result = simulate(lst, 10)
    assert result == expected


def test_long2():
    data = input.read_lines(day_num, 'test02.txt')
    expected = 36
    lst = (Command.parse(line) for line in data)
    result = simulate(lst, 10)
    assert result == expected
