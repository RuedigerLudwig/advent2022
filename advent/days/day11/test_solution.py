from advent.common import input

from .solution import Troop_While_Kinda_Relieved, Troop_While_Worried, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 10605
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 2713310158
    result = part2(lines)
    assert result == expected


def test_parse_all():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 4
    result = Troop_While_Worried.parse(lines)
    assert len(result.monkeys) == expected


def test_one_round():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = [2080, 25, 167, 207, 401, 1046]
    result = Troop_While_Worried.parse(lines)
    result.single_round()
    assert list(result.monkeys[1].items) == expected


def test_rounds():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 101
    result = Troop_While_Worried.parse(lines)
    result.rounds(20)
    assert result.monkeys[0].inspected == expected


def test_inspected():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 10605
    result = Troop_While_Worried.parse(lines)
    result.rounds(20)
    assert result.inspected_result() == expected


def test_inspected2():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 2713310158
    result = Troop_While_Kinda_Relieved.parse(lines)
    result.rounds(10_000)
    assert result.inspected_result() == expected
