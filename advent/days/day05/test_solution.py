from advent.common import utils

from .solution import Move, day_num, part1, part2, Crane


def test_part1():
    data = utils.read_data(day_num, 'test01.txt')
    expected = "CMZ"
    result = part1(data)
    assert result == expected


def test_part2():
    data = utils.read_data(day_num, 'test01.txt')
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
    data = utils.read_data(day_num, 'test01.txt')
    expected = ["ZN", "MCD", "P"]
    result = Crane.parse_drawing(data)
    assert result == expected


def test_parse_move():
    input = "move 1 from 2 to 1"
    expected = Move(1, 1, 0)
    result = Move.parse(input)
    assert result == expected


def test_parse_all():
    data = utils.read_data(day_num, 'test01.txt')
    expected = Crane(
        ["ZN", "MCD", "P"],
        [Move(1, 1, 0), Move(3, 0, 2), Move(2, 1, 0), Move(1, 0, 1)], True)
    result = Crane.parse(data, True)
    assert result == expected


def test_step():
    data = utils.read_data(day_num, 'test01.txt')
    state = Crane.parse(data, True)
    expected = ["ZND", "MC", "P"]
    result = state.moves[0].do_move(state.stacks, False)
    assert result == expected


def test_all_moves():
    data = utils.read_data(day_num, 'test01.txt')
    state = Crane.parse(data, False)
    expected = ["C", "M", "PDNZ"]
    result = state.perform_all_moves()
    assert result == expected


def test_all_moves9001():
    data = utils.read_data(day_num, 'test01.txt')
    state = Crane.parse(data, True)
    expected = ["M", "C", "PZND"]
    result = state.perform_all_moves()
    assert result == expected
