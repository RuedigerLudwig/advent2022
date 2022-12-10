from advent.common import utils

from .solution import Signal, day_num, part1, part2


def test_part1():
    lines = utils.read_data(day_num, 'test01.txt')
    expected = 13140
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = utils.read_data(day_num, 'test01.txt')
    expected = list(utils.read_data(day_num, 'expected.txt'))
    result = part2(lines)
    assert result == expected


def test_small():
    lines = utils.read_data(day_num, 'test02.txt')
    expected = [1, 1, 1, 4, 4]
    result = list(Signal.cycles(lines))
    assert result == expected


def test_grab_values():
    lines = utils.read_data(day_num, 'test01.txt')
    expected = [420, 1140, 1800, 2940, 2880, 3960]
    result = list(Signal.grab_values(lines))
    assert result == expected


def test_draw():
    lines = utils.read_data(day_num, 'test01.txt')
    expected = list(utils.read_data(day_num, 'expected.txt'))
    result = Signal.draw(lines, 40, 6)
    assert result == expected
