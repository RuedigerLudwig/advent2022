from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations

from typing import Iterator, Self

from advent.common.position import Position

day_num = 15


def part1(lines: Iterator[str]) -> int:
    row = int(next(lines))
    sensor_map = SensorMap.parse(lines)
    return sensor_map.count_impossible(row)


def part2(lines: Iterator[str]) -> int:
    next(lines)
    sensor_map = SensorMap.parse(lines)
    return sensor_map.get_possible_frequency()


ColRange = tuple[int, int]


@dataclass(slots=True, frozen=True)
class Sensor:
    number: int
    position: Position
    distance: int

    @classmethod
    def parse(cls, line: str, number: int) -> tuple[Self, Position]:
        parts = line.split('=')
        sensor = Position(int(parts[1].split(',')[0].strip()), int(parts[2].split(':')[0].strip()))
        beacon = Position(int(parts[3].split(',')[0].strip()), int(parts[4].strip()))
        return cls(number, sensor, sensor.taxicab_distance(beacon)), beacon

    def col_range_at_row(self, row: int) -> ColRange | None:
        col_distance = self.distance - abs(self.position.y - row)
        if col_distance < 0:
            return None

        from_x = self.position.x - col_distance
        to_x = self.position.x + col_distance

        return from_x, to_x

    def is_within(self, position: Position) -> bool:
        return self.position.taxicab_distance(position) <= self.distance


@dataclass(slots=True, frozen=True)
class ManhattenLine:
    start: Position
    direction_up: bool
    steps: int

    @classmethod
    def create(cls, start: Position, end: Position) -> ManhattenLine | None:
        if start.x > end.x:
            start, end = end, start
        steps_x = end.x - start.x
        steps_y = end.y - start.y
        if steps_x != abs(steps_y):
            return None
        return ManhattenLine(start, steps_y < 0, steps_x)

    def crosspoint(self, other: ManhattenLine) -> Position | None:
        if self.direction_up == other.direction_up:
            return None
        elif self.direction_up:
            bottom_up, top_down = self, other
        else:
            bottom_up, top_down = other, self

        r2 = bottom_up.start.x + bottom_up.start.y - (top_down.start.x + top_down.start.y)
        if r2 % 2 != 0:
            return None

        r = r2 // 2
        if r < 0 or r > top_down.steps:
            return None

        return top_down.start + Position.splat(r)


@dataclass(slots=True, frozen=True)
class SensorMap:
    sensors: list[Sensor]
    beacons: set[Position]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> SensorMap:
        sensors: list[Sensor] = []
        beacons: set[Position] = set()
        for number, line in enumerate(lines):
            sensor, beacon = Sensor.parse(line, number)
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
                    current = ColRange((current[0], col_range[1]))
        yield current

    def count_impossible(self, row: int) -> int:
        col_ranges = self.get_impossible(row)

        seen = sum(rng[1] - rng[0] + 1 for rng in SensorMap.merged_col_ranges(col_ranges))
        beacons = len({beacon.x for beacon in self.beacons if beacon.y == row})

        return seen - beacons

    @classmethod
    def tuning_frequency(cls, position: Position) -> int:
        return position.x * 4_000_000 + position.y

    @classmethod
    def get_midline(cls, sensor1: Sensor, sensor2: Sensor) -> ManhattenLine | None:
        distance = sensor1.position.taxicab_distance(sensor2.position)
        if distance != sensor1.distance + sensor2.distance + 2:
            return None

        if sensor1.position.x == sensor2.position.x or sensor1.position.y == sensor2.position.y:
            return None  # Don't know how to handle that now, maybe include later

        if sensor1.position.x > sensor2.position.x:
            sensor1, sensor2 = sensor2, sensor1

        if sensor1.position.y < sensor2.position.y:
            if sensor1.distance < sensor2.distance:
                return ManhattenLine.create(Position(sensor1.position.x + sensor1.distance + 1,
                                                     sensor1.position.y),
                                            Position(sensor1.position.x,
                                                     sensor1.position.y + sensor1.distance + 1))
            else:
                return ManhattenLine.create(Position(sensor2.position.x - sensor2.distance - 1,
                                                     sensor2.position.y),
                                            Position(sensor2.position.x,
                                                     sensor2.position.y - sensor2.distance - 1))
        else:
            if sensor1.distance < sensor2.distance:
                return ManhattenLine.create(Position(sensor1.position.x,
                                                     sensor1.position.y - sensor1.distance - 1),
                                            Position(sensor1.position.x + sensor1.distance + 1,
                                                     sensor1.position.y))
            else:
                return ManhattenLine.create(Position(sensor2.position.x,
                                                     sensor2.position.y + sensor2.distance + 1),
                                            Position(sensor2.position.x - sensor2.distance - 1,
                                                     sensor2.position.y))

    def get_possible_frequency(self) -> int:
        midlines: list[ManhattenLine] = []
        for sensor1, sensor2 in combinations(self.sensors, 2):
            midline = SensorMap.get_midline(sensor1, sensor2)
            if midline is not None:
                midlines.append(midline)
        for line1, line2 in combinations(midlines, 2):
            point = line1.crosspoint(line2)
            if point is not None and all(not sensor.is_within(point) for sensor in self.sensors):
                return SensorMap.tuning_frequency(point)

        raise Exception("No point found")
