from advent.common import input

from .solution import day_num, part1, part2, Shape, Result


def test_part1():
    data = input.read_lines(day_num, 'test01.txt')
    expected = 15
    result = part1(data)
    assert result == expected


def test_part2():
    data = input.read_lines(day_num, 'test01.txt')
    expected = 12
    result = part2(data)
    assert result == expected


def test_parse_line():
    input = "A Y"
    expected = Shape.Rock, Shape.Paper
    result = Shape.parse(input)
    assert result == expected


def test_round1():
    input = "A Y"
    expected = 8
    opponent, player = Shape.parse(input)
    assert player.score(opponent) == expected


def test_round2():
    input = "A Y"
    expected = Shape.Rock
    opponent, result = Result.parse(input)
    assert result.player_shape(opponent) == expected


def test_round3():
    input = "B X"
    expected = 1
    opponent, result = Result.parse(input)
    assert result.player_shape(opponent).score(opponent) == expected
