from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum
from queue import PriorityQueue

from typing import Iterator

from advent.common.position import UNIT_NEG_X, UNIT_NEG_Y, UNIT_X, UNIT_Y, Position


day_num = 24


def part1(lines: Iterator[str]) -> int:
    valley = Valley.parse(lines)
    return valley.find_way(1)


def part2(lines: Iterator[str]) -> int:
    valley = Valley.parse(lines)
    return valley.find_way(3)


def gcd(num1: int, num2: int) -> int:
    assert num1 >= 0 and num2 >= 0
    if num1 == 0 or num2 == 0:
        return 0
    while num2 != 0:
        num1, num2 = num2, num1 % num2
    return num1


def lcm(num1: int, num2: int) -> int:
    return num1 * num2 // gcd(num1, num2)


BlizList = list[Position]
BlizTuple = tuple[BlizList, BlizList, BlizList, BlizList]


class Direction(IntEnum):
    East = 0
    North = 1
    West = 2
    South = 3

    @classmethod
    def create(cls, char: str) -> Direction:
        match char:
            case '>': return Direction.East
            case '^': return Direction.North
            case '<': return Direction.West
            case 'v': return Direction.South
            case _: raise Exception("Illegal Direction")

    def position(self) -> Position:
        match self:
            case Direction.East: return UNIT_X
            case Direction.North: return UNIT_NEG_Y
            case Direction.West: return UNIT_NEG_X
            case Direction.South: return UNIT_Y

    @property
    def char(self) -> str:
        match self:
            case Direction.East: return ">"
            case Direction.North: return "^"
            case Direction.West: return "<"
            case Direction.South: return "v"


@dataclass(slots=True, frozen=True)
class Weather:
    blizzards: list[dict[Position, str]] = field(repr=False)
    extent: Position
    repeat: int

    def print(self, time: int) -> list[str]:
        current = self.blizzards[self.normal_time(time)]
        lines: list[str] = []
        for row in range(self.extent.y):
            line = ""
            for col in range(self.extent.x):
                if (char := current.get(Position(col, row))) is not None:
                    line += char
                else:
                    line += '.'
            lines.append(line)
        return lines

    def normal_time(self, time: int) -> int:
        return time % self.repeat

    def get(self, time: int) -> dict[Position, str]:
        return self.blizzards[time % self.repeat]

    @classmethod
    def predict_weather(cls, blizzards: BlizTuple, extent: Position) -> Weather:
        repeat = lcm(extent.x, extent.y)
        weather: list[dict[Position, str]] = [Weather.create_dict(blizzards)]
        for _ in range(repeat - 1):
            blizzards = Weather.progress_blizzards(blizzards, extent)
            weather.append(Weather.create_dict(blizzards))

        return Weather(weather, extent, repeat)

    @classmethod
    def move_east(cls, blizzards: BlizList, extent: Position) -> BlizList:
        add = Direction.East.position()
        result: BlizList = []
        for pos in blizzards:
            next_pos = pos + add
            if next_pos.x >= extent.x:
                next_pos = next_pos.set_x(0)
            result.append(next_pos)

        return result

    @classmethod
    def move_west(cls, blizzards: BlizList, extent: Position) -> BlizList:
        add = Direction.West.position()
        result: BlizList = []
        for pos in blizzards:
            next_pos = pos + add
            if next_pos.x < 0:
                next_pos = next_pos.set_x(extent.x - 1)
            result.append(next_pos)

        return result

    @classmethod
    def move_south(cls, blizzards: BlizList, extent: Position) -> BlizList:
        add = Direction.South.position()
        result: BlizList = []
        for pos in blizzards:
            next_pos = pos + add
            if next_pos.y >= extent.y:
                next_pos = next_pos.set_y(0)
            result.append(next_pos)

        return result

    @classmethod
    def move_north(cls, blizzards: BlizList, extent: Position) -> BlizList:
        add = Direction.North.position()
        result: BlizList = []
        for pos in blizzards:
            next_pos = pos + add
            if next_pos.y < 0:
                next_pos = next_pos.set_y(extent.y - 1)
            result.append(next_pos)

        return result

    @classmethod
    def _add_list(cls, map: dict[Position, str], lst: BlizList, char: str) -> dict[Position, str]:
        for position in lst:
            match map.get(position):
                case None: map[position] = char
                case '2': map[position] = '3'
                case '3': map[position] = '4'
                case _: map[position] = '2'
        return map

    @classmethod
    def create_dict(cls, blizzards: BlizTuple) -> dict[Position, str]:
        map = Weather._add_list({}, blizzards[0], Direction.East.char)
        map = Weather._add_list(map, blizzards[1], Direction.North.char)
        map = Weather._add_list(map, blizzards[2], Direction.West.char)
        return Weather._add_list(map, blizzards[3], Direction.South.char)

    @classmethod
    def progress_blizzards(cls, blizzards: BlizTuple, extent: Position) -> BlizTuple:
        return (
            Weather.move_east(blizzards[0], extent),
            Weather.move_north(blizzards[1], extent),
            Weather.move_west(blizzards[2], extent),
            Weather.move_south(blizzards[3], extent),
        )


@dataclass(slots=True, frozen=True)
class Valley:
    weather: Weather = field(repr=False)
    extent: Position
    start: Position
    exit: Position

    @classmethod
    def append(cls, blizzards: BlizTuple, direction: Direction, position: Position) -> BlizTuple:
        return tuple(
            directed if num != direction else directed + [position]
            for num, directed in enumerate(blizzards)
        )

    @classmethod
    def _get_wallbreak(cls, lines: str) -> int:
        for col, tile in enumerate(lines[1:]):
            if tile == '.':
                return col
        raise Exception("No break in the wall")

    @classmethod
    def parse_line(cls, blizzards: BlizTuple, line: str, row: int) -> BlizTuple:
        for col, char in enumerate(line[1:]):
            match char:
                case '#':
                    return blizzards
                case '>' | '^' | '<' | 'v':
                    blizzards = Valley.append(blizzards, Direction.create(char), Position(col, row))
                case '.':
                    pass
                case _:
                    raise Exception("Unknown char: {char}")

        raise Exception("line not terminated by wall")

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Valley:
        first_line = next(lines)
        start_col = Valley._get_wallbreak(first_line)
        width = len(first_line) - 2
        blizzards: BlizTuple = [], [], [], []
        for row, line in enumerate(lines):
            if line.startswith("##"):
                end_col = Valley._get_wallbreak(line)
                extent = Position(width, row)
                return Valley(Weather.predict_weather(blizzards, extent), extent,
                              Position(start_col, -1), Position(end_col, row))
            else:
                blizzards = Valley.parse_line(blizzards, line, row)
        assert False, "Unreachable"

    def __str__(self) -> str:
        return '\n'.join(self.print(0))

    def print(self, time: int) -> list[str]:
        first = '#' + ('#' * self.start.x) + '.' + ('#' * (self.extent.x - self.start.x))
        last = '#' + ('#' * self.exit.x) + '.' + ('#' * (self.extent.x - self.exit.x))
        lines = self.weather.print(time)
        lines = [first] + ['#' + line + '#' for line in lines] + [last]
        return lines

    def find_way(self, rounds: int) -> int:
        queue: PriorityQueue[Step] = PriorityQueue()
        queue.put(Step(
            position=self.start,
            time=0,
            round=0,
            valley=self,
            start=self.start,
            target=self.exit))
        reached: set[tuple[Position, int, int]] = set()
        while not queue.empty():
            current = queue.get()
            if current.round == rounds:
                return current.time

            normal_time = self.weather.normal_time(current.time)
            if (current.position, normal_time, current.round) in reached:
                continue

            reached.add((current.position, normal_time, current.round))
            for next in current.possible_moves():
                queue.put(next)

        raise Exception("No path found")


@dataclass(slots=True, kw_only=True)
class Step:
    position: Position
    time: int
    round: int
    start: Position
    target: Position
    valley: Valley

    def __lt__(self, other: Step) -> bool:
        return self.time < other.time

    def __str__(self) -> str:
        return '\n'.join(self.print())

    def print(self) -> list[str]:
        lines = self.valley.print(self.time)

        line = lines[self.position.y + 1]
        lines[self.position.y + 1] = line[:self.position.x + 1] + \
            'E' + line[self.position.x + 2:]

        return lines

    def reach_target(self) -> Step:
        path = Step(position=self.target,
                    time=self.time + 1,
                    round=self.round + 1,
                    valley=self.valley,
                    start=self.target,
                    target=self.start,
                    )
        return path

    def move(self, position: Position) -> Step:
        return Step(position=position,
                    time=self.time + 1,
                    round=self.round,
                    valley=self.valley,
                    start=self.start,
                    target=self.target,
                    )

    def wait(self) -> Step:
        return Step(position=self.position,
                    time=self.time + 1,
                    round=self.round,
                    valley=self.valley,
                    start=self.start,
                    target=self.target,
                    )

    def possible_moves(self) -> Iterator[Step]:
        impassable = self.valley.weather.get(self.time + 1)

        if self.position not in impassable:
            yield self.wait()

        for dir in Direction:
            add = dir.position()
            next_position = self.position + add
            if next_position == self.target:
                yield self.reach_target()

            elif (0 <= next_position.x < self.valley.extent.x
                    and 0 <= next_position.y < self.valley.extent.y):
                if next_position not in impassable:
                    yield self.move(next_position)
