from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

from typing import Iterator, Self

day_num = 22


def part1(lines: Iterator[str]) -> int:
    jungle = PasswordSimpleJungle.create(lines)
    return jungle.walk().value


def part2(lines: Iterator[str]) -> int:
    jungle = PasswordCubeJungle.create(lines)
    return jungle.walk().value


class Turn(Enum):
    Left = 1
    Right = 2


class Facing(Enum):
    Right = 0
    Down = 1
    Left = 2
    Up = 3

    def turn(self, turn: Turn) -> Facing:
        match turn:
            case Turn.Left:
                match self:
                    case Facing.Right: return Facing.Up
                    case Facing.Up: return Facing.Left
                    case Facing.Left: return Facing.Down
                    case Facing.Down: return Facing.Right
            case Turn.Right:
                match self:
                    case Facing.Right: return Facing.Down
                    case Facing.Up: return Facing.Right
                    case Facing.Left: return Facing.Up
                    case Facing.Down: return Facing.Left

    def as_position(self) -> Position2D:
        match self:
            case Facing.Right: return Position2D(1, 0)
            case Facing.Up: return Position2D(0, -1)
            case Facing.Left: return Position2D(-1, 0)
            case Facing.Down: return Position2D(0, 1)


@dataclass(slots=True, frozen=True)
class Position2D:
    x: int
    y: int

    def __add__(self, other: Position2D) -> Position2D:
        return Position2D(self.x + other.x, self.y + other.y)

    def __mul__(self, factor: int) -> Position2D:
        return Position2D(self.x * factor, self.y * factor)


@dataclass(slots=True, frozen=True)
class Player:
    position: Position2D
    facing: Facing

    @property
    def value(self) -> int:
        return (self.position.y + 1) * 1000 + (self.position.x + 1) * 4 + self.facing.value

    def turn(self, direction: Turn) -> Player:
        return Player(self.position, self.facing.turn(direction))

    def step(self) -> Player:
        return Player(self.position + self.facing.as_position(), self.facing)


@dataclass(slots=True)
class PasswordJungle(ABC):
    map: list[str]
    instructions: str

    @abstractmethod
    def wrap(self, player: Player) -> Player:
        ...

    @classmethod
    def create(cls, lines: Iterator[str]) -> Self:
        map: list[str] = []
        for line in lines:
            if not line:
                break
            map.append(line)
        return cls(map, next(lines))

    def next_instruction(self, start: int) -> tuple[int | Turn, int] | None:
        if start >= len(self.instructions):
            return None
        match self.instructions[start]:
            case 'L': return Turn.Left, start + 1
            case 'R': return Turn.Right, start + 1
            case d if d.isdecimal():
                val = int(d)
                start += 1
                while start < len(self.instructions) and self.instructions[start].isdecimal():
                    val = val * 10 + int(self.instructions[start])
                    start += 1
                return val, start
            case _: raise Exception("Illegal char")

    def start(self) -> tuple[Position2D, Facing]:
        return self.start_column(0), Facing.Right

    def start_column(self, row: int) -> Position2D:
        for col, char in enumerate(self.map[row]):
            if char != ' ':
                return Position2D(col, row)
        raise Exception("Empty row found")

    def end_column(self, row: int) -> Position2D:
        for col in range(len(self.map[row]) - 1, -1, -1):
            if self.map[row][col] != ' ':
                return Position2D(col, row)
        raise Exception("Empty row found")

    def start_row(self, col: int) -> Position2D:
        for row, line in enumerate(self.map):
            if col < len(line) and line[col] != ' ':
                return Position2D(col, row)
        raise Exception("Empty row found")

    def end_row(self, col: int) -> Position2D:
        for row in range(len(self.map) - 1, -1, -1):
            line = self.map[row]
            if col < len(line) and line[col] != ' ':
                return Position2D(col, row)
        raise Exception("Empty row found")

    def check_tile(self, pos: Position2D) -> str:
        if pos.y not in range(0, len(self.map)) or pos.x not in range(0, len(self.map[pos.y])):
            return ' '
        return self.map[pos.y][pos.x]

    def step(self, player: Player, steps: int) -> Player:
        for _ in range(steps):
            player_next = player.step()
            finished = False
            while not finished:
                match self.check_tile(player_next.position):
                    case '#':
                        return player
                    case '.':
                        player = player_next
                        finished = True
                    case ' ':
                        player_next = self.wrap(player)
                    case _: assert False, "Unreachable"
        return player

    def walk(self) -> Player:
        start, facing = self.start()
        player = Player(start, facing)
        instruct_pos = 0

        while (next := self.next_instruction(instruct_pos)) is not None:
            instruction, instruct_pos = next
            match instruction:
                case int(steps): player = self.step(player, steps)
                case turn: player = player.turn(turn)
        return player


def max_width(map: list[str]) -> int:
    return max(len(row) for row in map)


@dataclass(slots=True, frozen=True)
class Vector:
    x: int
    y: int
    z: int

    def __neg__(self: Vector) -> Vector:
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, other: Vector) -> Vector:
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)


@dataclass(slots=True, frozen=True)
class CubePosition:
    side: Vector
    facing: Vector

    def forward(self) -> CubePosition:
        return CubePosition(self.facing, -self.side)

    def turn(self, direction: Turn) -> CubePosition:
        if direction == Turn.Left:
            return CubePosition(self.side, self.vertical)
        else:
            return CubePosition(self.side, -self.vertical)

    @property
    def vertical(self) -> Vector:
        return self.side * self.facing


@dataclass(slots=True)
class PasswordCubeJungle(PasswordJungle):
    cube_width: int = field(default=50, init=False)
    sides: dict[Vector, tuple[Position2D, Vector]] = field(default_factory=dict, init=False)

    def _find_neighbors(self, map_position: Position2D, facing: Facing,
                        cube_position: CubePosition):
        match facing:
            case Facing.Right: facing_right = cube_position.facing
            case Facing.Up: facing_right = -cube_position.vertical
            case Facing.Left: facing_right = -cube_position.facing
            case Facing.Down: facing_right = cube_position.vertical
        self.sides[cube_position.side] = map_position, facing_right
        if len(self.sides) == 6:
            return

        for _ in range(4):
            next_position = map_position + facing.as_position() * self.cube_width
            if self.check_tile(next_position) != ' ':
                next_cube = cube_position.forward()
                if next_cube.side not in self.sides:
                    self._find_neighbors(next_position, facing, next_cube)

            facing = facing.turn(Turn.Left)
            cube_position = cube_position.turn(Turn.Left)

    def __post_init__(self):
        width = max_width(self.map)
        if len(self.map) % 3 == 0:
            assert width % 4 == 0
            self.cube_width = len(self.map) // 3
        elif width % 3 == 0:
            assert len(self.map) % 4 == 0
            self.cube_width = width // 3
        else:
            assert False, "Unknown cube dimensions"

        start, facing = self.start()
        self._find_neighbors(
            start, facing,
            CubePosition(Vector(1, 0, 0), Vector(0, 1, 0)))

    def get_cube_position(self, player: Player) -> tuple[CubePosition, int]:
        for side, (start, right) in self.sides.items():
            if (start.x <= player.position.x < start.x + self.cube_width
                    and start.y <= player.position.y < start.y + self.cube_width):
                match player.facing:
                    case Facing.Right:
                        delta = player.position.y - start.y
                    case Facing.Up:
                        delta = player.position.x - start.x
                        right = -right * side
                    case Facing.Left:
                        delta = start.y + self.cube_width - 1 - player.position.y
                        right = -right
                    case Facing.Down:
                        delta = start.x + self.cube_width - 1 - player.position.x
                        right = right * side
                return CubePosition(side, right), delta
        raise Exception("Not a legal position for the player")

    def wrap(self, player: Player) -> Player:
        old, delta = self.get_cube_position(player)
        new = old.forward()
        position, normal_right = self.sides[new.side]
        normal = CubePosition(new.side, normal_right)

        if new.facing == normal.facing:
            facing = Facing.Right
            x = position.x
            y = position.y + delta

        elif new.facing == -normal.facing:
            facing = Facing.Left
            x = position.x + self.cube_width - 1
            y = position.y + self.cube_width - 1 - delta

        elif new.facing == normal.vertical:
            facing = Facing.Up
            y = position.y + self.cube_width - 1
            x = position.x + delta

        else:
            facing = Facing.Down
            y = position.y
            x = position.x + self.cube_width - 1 - delta

        result = Player(Position2D(x, y), facing)
        return result


@dataclass(slots=True)
class PasswordSimpleJungle(PasswordJungle):
    def wrap(self, player: Player) -> Player:
        match player.facing:
            case Facing.Right:
                return Player(self.start_column(player.position.y), Facing.Right)
            case Facing.Down:
                return Player(self.start_row(player.position.x), Facing.Down)
            case Facing.Left:
                return Player(self.end_column(player.position.y), Facing.Left)
            case Facing.Up:
                return Player(self.end_row(player.position.x), Facing.Up)
