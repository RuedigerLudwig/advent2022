from advent.common import input

from .solution import Cave, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 3068
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 1514285714288
    result = part2(lines)
    assert result == expected


def test_first():
    input = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    cave = Cave.create(7, input)
    cave.process_one_rock()
    expected = "  #### "
    assert cave.cave[0] == expected


def test_third():
    input = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    cave = Cave.create(7, input)
    height = cave.process_many_rocks(3)
    expected = "####   "
    assert cave.cave[3] == expected
    assert height == 6
