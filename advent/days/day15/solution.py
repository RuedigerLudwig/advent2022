from __future__ import annotations
from dataclasses import dataclass

from typing import Iterator, Self

from advent.common.position import Position

day_num = 15


def part1(lines: Iterator[str]) -> int:
    row, _ = next(lines).split('/')
    sensor_map = SensorMap.parse(lines)
    return sensor_map.count_impossible(int(row))


def part2(lines: Iterator[str]) -> int:
    _, max_range = next(lines).split('/')
    sensor_map = SensorMap.parse(lines)
    return sensor_map.get_possible_frequency(int(max_range))


ColRange = tuple[int, int]


@dataclass(slots=True, frozen=True)
class Sensor:
    sensor: Position
    distance: int

    @classmethod
    def parse(cls, line: str) -> tuple[Self, Position]:
        parts = line.split('=')
        sensor = Position(int(parts[1].split(',')[0].strip()), int(parts[2].split(':')[0].strip()))
        beacon = Position(int(parts[3].split(',')[0].strip()), int(parts[4].strip()))
        return cls(sensor, sensor.taxicab_distance(beacon)), beacon

    def col_range_at_row(self, row: int) -> ColRange | None:
        col_distance = self.distance - abs(self.sensor.y - row)
        if col_distance < 0:
            return None

        from_x = self.sensor.x - col_distance
        to_x = self.sensor.x + col_distance

        return from_x, to_x


@dataclass(slots=True, frozen=True)
class SensorMap:
    sensors: list[Sensor]
    beacons: set[Position]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> SensorMap:
        sensors: list[Sensor] = []
        beacons: set[Position] = set()
        for line in lines:
            sensor, beacon = Sensor.parse(line)
            sensors.append(sensor)
            beacons.add(beacon)
        return cls(sensors, beacons)

    def get_impossible(self, row: int) -> list[ColRange]:
        col_ranges: list[ColRange] = []

        for sensor in self.sensors:
            x_range = sensor.col_range_at_row(row)
            if x_range is None:
                continue
            from_x, to_x = x_range
            col_ranges.append((from_x, to_x))

        return col_ranges

    @classmethod
    def merged_col_ranges(cls, col_ranges: list[ColRange]) -> Iterator[ColRange]:
        col_ranges = sorted(col_ranges)
        current = col_ranges[0]
        for col_range in col_ranges:
            if current[1] < col_range[1]:
                if current[1] < col_range[0]:
                    yield current
                    current = col_range
                else:
                    current = current[0], col_range[1]
        yield current

    def count_impossible(self, row: int) -> int:
        col_ranges = self.get_impossible(row)

        seen = sum(rng[1] - rng[0] + 1 for rng in SensorMap.merged_col_ranges(col_ranges))
        beacons = len({beacon.x for beacon in self.beacons if beacon.y == row})

        return seen - beacons

    def get_possible(self, max_range: int) -> Position:
        for row in range(max_range):
            col_ranges = sorted(self.get_impossible(row))

            curr1 = col_ranges[0][1]
            for one0, one1 in col_ranges:
                if curr1 < one1:
                    if curr1 < one0:
                        return Position(curr1 + 1, row)
                    if one1 > max_range:
                        break
                    curr1 = one1

        raise Exception("No best spot found")

    def get_possible_frequency(self, max_range: int) -> int:
        freq_x, freq_y = self.get_possible(max_range)
        return freq_x * 4_000_000 + freq_y
