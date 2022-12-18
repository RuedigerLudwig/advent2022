from advent.common import input

from .solution import Position, Shower, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 64
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 58
    result = part2(lines)
    assert result == expected


def test_simple_count():
    lines = ["1,1,1", "1,1,2"]
    expected = 10
    result = Shower.create(Position.parse_all(lines))
    assert result.faces == expected


def test_example_faces():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 64
    result = Shower.create(Position.parse_all(lines))
    assert result.faces == expected


def test_example_trapped():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 6
    result = Shower.create(Position.parse_all(lines))
    assert result.count_trapped_droplets() == expected
