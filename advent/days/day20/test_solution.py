from advent.common import input

from .solution import Ring, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 3
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 1623178306
    result = part2(lines)
    assert result == expected


def test_once():
    lines = (int(line) for line in input.read_lines(day_num, 'example01.txt'))
    ring = Ring.create(lines)
    ring.process(1)

    expected = [0, 3, -2, 1, 2, -3, 4]
    assert list(ring.zero.stopping()) == expected


def test_get_odered():
    lines = (int(line) for line in input.read_lines(day_num, 'example01.txt'))
    ring = Ring.create(lines)
    ring.process(1)

    expected = [4, -3, 2]
    assert list(ring.get_ordered([1000, 2000, 3000])) == expected
