from advent.common import input

from .solution import Network, RawValve, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 1651
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 1707
    result = part2(lines)
    assert result == expected


def test_parse():
    line = "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"
    expected = RawValve("AA", 0, ["DD", "II", "BB"])
    result = RawValve.parse(line)
    assert result == expected


def test_open_system():
    lines = input.read_lines(day_num, 'example01.txt')
    system = Network.parse(lines)
    expected = 1651
    assert system.under_pressure(30, 1) == expected


def test_open_system_elephant():
    lines = input.read_lines(day_num, 'example01.txt')
    system = Network.parse(lines)
    expected = 1707
    assert system.under_pressure(26, 2) == expected
