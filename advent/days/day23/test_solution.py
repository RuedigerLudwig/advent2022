from advent.common import input

from .solution import Ground, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 110
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 20
    result = part2(lines)
    assert result == expected


def test_round1():
    lines = input.read_lines(day_num, 'example02.txt')
    ground = Ground.parse(lines)
    expected = "##\n..\n#.\n.#\n#."
    ground.rounds(1)
    assert str(ground) == expected


def test_round10():
    ground = Ground.parse(input.read_lines(day_num, 'example01.txt'))
    expected = Ground.parse(input.read_lines(day_num, 'expected01_10.txt'))
    ground.rounds(10)
    assert str(ground) == str(expected)


def test_round2():
    lines = input.read_lines(day_num, 'example02.txt')
    ground = Ground.parse(lines)
    expected = ".##.\n#...\n...#\n....\n.#.."
    ground.rounds(2)
    assert str(ground) == expected
