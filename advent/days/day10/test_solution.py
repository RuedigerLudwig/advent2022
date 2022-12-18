from advent.common import input

from .solution import cycles, day_num, draw, grab_values, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 13140
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = list(input.read_lines(day_num, 'expected01.txt'))
    result = part2(lines)
    assert result == expected


def test_small():
    lines = input.read_lines(day_num, 'example02.txt')
    expected = [1, 1, 1, 4, 4, -1]
    result = list(cycles(lines))
    assert result == expected


def test_grab_values():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = [420, 1140, 1800, 2940, 2880, 3960]
    result = list(grab_values(lines))
    assert result == expected


def test_draw():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = list(input.read_lines(day_num, 'expected01.txt'))
    result = draw(lines, 40, 6)
    assert result == expected
