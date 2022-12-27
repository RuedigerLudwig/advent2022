from advent.common import input

from .solution import BlizTuple, Valley, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 18
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 54
    result = part2(lines)
    assert result == expected


def test_parse_line():
    input = "#>>.<^<#"
    expected: BlizTuple = (
        [(0, 0), (1, 0)],
        [(4, 0)],
        [(3, 0), (5, 0)],
        [])
    result = Valley.parse_line(([], [], [], []), input, 0)
    assert result == expected


def test_walk():
    lines = input.read_lines(day_num, 'example01.txt')
    valley = Valley.parse(lines)
    result = valley.find_way(1)
    assert result == 18


def test_walk2():
    lines = input.read_lines(day_num, 'example01.txt')
    valley = Valley.parse(lines)
    result = valley.find_way(2)
    assert result == (18 + 23)


def test_back_and_forth():
    lines = input.read_lines(day_num, 'example01.txt')
    valley = Valley.parse(lines)
    result = valley.find_way(3)
    assert result == 54
