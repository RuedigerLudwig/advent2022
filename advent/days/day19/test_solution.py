from advent.common import input

from .solution import Blueprint, day_num, part1, part2
import pytest


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 33
    result = part1(lines)
    assert result == expected


@pytest.mark.skip
def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = (56 * 62)
    result = part2(lines)
    assert result == expected


def test_parse():
    lines = input.read_lines(day_num, 'example01.txt')
    blueprint = Blueprint.parse(next(lines))
    expected = Blueprint(1, ((0, 7, 0, 2), (0, 0, 14, 3),
                         (0, 0, 0, 2), (0, 0, 0, 4)), (0, 7, 14, 4))
    assert blueprint == expected


def test_blueprint1():
    lines = input.read_lines(day_num, 'example01.txt')
    blueprint = Blueprint.parse(next(lines))
    expected = 9
    result = blueprint.run(24)
    assert result == expected


@pytest.mark.skip
def test_blueprint2():
    lines = input.read_lines(day_num, 'example01.txt')
    next(lines)
    blueprint = Blueprint.parse(next(lines))
    expected = 12
    result = blueprint.run(24)
    assert result == expected
