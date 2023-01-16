from advent.common import input
from advent.common.position import Position

from .solution import Sensor, SensorMap, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 26
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 56000011
    result = part2(lines)
    assert result == expected


def test_parse():
    input = "Sensor at x=2, y=18: closest beacon is at x=-2, y=15"
    expected = Sensor(1, Position(2, 18), 7), Position(-2, 15)
    result = Sensor.parse(input, 1)
    assert result == expected


def test_x_range():
    input = "Sensor at x=8, y=7: closest beacon is at x=2, y=10"
    sensor, _ = Sensor.parse(input, 1)
    assert sensor.col_range_at_row(10) == (2, 14)
    assert sensor.col_range_at_row(11) == (3, 13)


def test_impossible():
    lines = input.read_lines(day_num, 'example01.txt')
    next(lines)
    sensor_map = SensorMap.parse(lines)
    expected = 26
    result = sensor_map.count_impossible(10)
    assert result == expected


def test_possible():
    lines = input.read_lines(day_num, 'example01.txt')
    next(lines)
    sensor_map = SensorMap.parse(lines)
    expected = 56000011
    result = sensor_map.get_possible_frequency(20)
    assert result == expected
