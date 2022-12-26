from advent.common import input

from .solution import (
    CubePosition,
    Facing,
    PasswordCubeJungle,
    PasswordSimpleJungle,
    Player,
    Position2D,
    Vector,
    day_num,
    part1,
    part2)


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 6032
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 5031
    result = part2(lines)
    assert result == expected


def test_parse():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = "10R5L5R10L4R5L5"
    result = PasswordSimpleJungle.create(lines)
    assert result.instructions == expected


def test_next():
    lines = input.read_lines(day_num, 'example01.txt')
    jungle = PasswordSimpleJungle.create(lines)
    result = jungle.next_instruction(0)
    assert result == (10, 2)

    result = jungle.next_instruction(2)
    assert result == ('R', 3)

    result = jungle.next_instruction(14)
    assert result == (5, 15)

    result = jungle.next_instruction(15)
    assert result is None


def test_positions():
    lines = input.read_lines(day_num, 'example01.txt')
    jungle = PasswordSimpleJungle.create(lines)

    result = jungle.start_column(0)
    assert result == Position2D(8, 0)

    result = jungle.start_row(0)
    assert result == Position2D(0, 4)

    result = jungle.end_column(4)
    assert result == Position2D(11, 4)

    result = jungle.end_row(4)
    assert result == Position2D(4, 7)

    result = jungle.start_row(8)
    assert result == Position2D(8, 0)


def test_step():
    lines = input.read_lines(day_num, 'example01.txt')
    jungle = PasswordSimpleJungle.create(lines)
    person = jungle.step(Player(Position2D(8, 0), Facing.Right), 10)
    assert person == Player(Position2D(10, 0), Facing.Right)

    person = jungle.step(Player(Position2D(10, 0), Facing.Down), 5)
    assert person == Player(Position2D(10, 5), Facing.Down)

    person = jungle.step(Player(Position2D(10, 5), Facing.Right), 5)
    assert person == Player(Position2D(3, 5), Facing.Right)


def test_walk():
    lines = input.read_lines(day_num, 'example01.txt')
    jungle = PasswordSimpleJungle.create(lines)
    person = jungle.walk()
    assert person == Player(Position2D(7, 5), Facing.Right)
    assert person.value == 6032


def test_cube_width():
    lines = input.read_lines(day_num, 'example01.txt')
    jungle = PasswordCubeJungle.create(lines)
    assert jungle.cube_width == 4


def test_cube_info():
    lines = input.read_lines(day_num, 'example01.txt')
    jungle = PasswordCubeJungle.create(lines)

    person = Player(Position2D(14, 8), Facing.Up)
    result = jungle.get_cube_position(person)
    assert result == (CubePosition(Vector(0, 1, 0), Vector(0, 0, 1)), 2)

    person = Player(Position2D(11, 5), Facing.Right)
    result = jungle.get_cube_position(person)
    assert result == (CubePosition(Vector(0, 0, 1), Vector(0, 1, 0)), 2)

    person = Player(Position2D(1, 7), Facing.Down)
    result = jungle.get_cube_position(person)
    assert result == (CubePosition(Vector(0, 0, -1), Vector(-1, 0, 0)), 2)

    person = Player(Position2D(10, 11), Facing.Down)
    result = jungle.get_cube_position(person)
    assert result == (CubePosition(Vector(-1, 0, 0), Vector(0, 0, -1)), 1)


def test_cube_wrap():
    lines = input.read_lines(day_num, 'example01.txt')
    jungle = PasswordCubeJungle.create(lines)

    person = Player(Position2D(14, 8), Facing.Up)
    result = jungle.wrap(person)
    assert result == Player(Position2D(11, 5), Facing.Left)

    person = Player(Position2D(11, 5), Facing.Right)
    result = jungle.wrap(person)
    assert result == Player(Position2D(14, 8), Facing.Down)

    person = Player(Position2D(1, 7), Facing.Down)
    result = jungle.wrap(person)
    assert result == Player(Position2D(10, 11), Facing.Up)

    person = Player(Position2D(10, 11), Facing.Down)
    result = jungle.wrap(person)
    assert result == Player(Position2D(1, 7), Facing.Up)
