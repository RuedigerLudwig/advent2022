from advent.common import input

from .solution import Move, day_num, part1, part2, Crane


def test_part1():
    data = input.read_lines(day_num, 'test01.txt')
    expected = "CMZ"
    result = part1(data)
    assert result == expected


def test_part2():
    data = input.read_lines(day_num, 'test01.txt')
    expected = "MCD"
    result = part2(data)
    assert result == expected


def test_parse_line():
    input = "    [D]    "
    expected = [None, 'D', None]
    result = Crane.parse_crate_row(input)
    assert result == expected


def test_parse_line2():
    input = "[Z] [M] [P]"
    expected = ["Z", 'M', "P"]
    result = Crane.parse_crate_row(input)
    assert result == expected


def test_drawing():
    data = input.read_lines(day_num, 'test01.txt')
    expected = ["ZN", "MCD", "P"]
    result = Crane.parse_stacks(data)
    assert result == expected


def test_parse_move():
    input = "move 1 from 2 to 1"
    expected = Move(1, 1, 0)
    result = Move.parse(input)
    assert result == expected


def test_parse_all():
    data = input.read_lines(day_num, 'test01.txt')
    expected = Crane(
        ["ZN", "MCD", "P"],
        [Move(1, 1, 0), Move(3, 0, 2), Move(2, 1, 0), Move(1, 0, 1)], True)
    result = Crane.parse(data, True)
    assert result == expected


def test_all_moves():
    data = input.read_lines(day_num, 'test01.txt')
    crane = Crane.parse(data, False)
    expected = ["C", "M", "PDNZ"]
    result = crane.perform_all_moves()
    assert result == expected


def test_all_moves9001():
    data = input.read_lines(day_num, 'test01.txt')
    crane = Crane.parse(data, True)
    expected = ["M", "C", "PZND"]
    result = crane.perform_all_moves()
    assert result == expected
