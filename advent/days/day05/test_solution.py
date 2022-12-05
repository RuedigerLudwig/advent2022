from advent.common import utils

from .solution import day_num, part1, part2, State


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
    result = State.parse_crate_line(input)
    assert result == expected


def test_parse_line2():
    input = "[Z] [M] [P]"
    expected = ["Z", 'M', "P"]
    result = State.parse_crate_line(input)
    assert result == expected


def test_drawing():
    data = utils.read_data(day_num, 'test01.txt')
    expected = ["ZN", "MCD", "P"]
    result = State.parse_drawing(data)
    assert result == expected


def test_parse_move():
    input = "move 1 from 2 to 1"
    expected = 1, 1, 0
    result = State.parse_move(input)
    assert result == expected


def test_parse_all():
    data = utils.read_data(day_num, 'test01.txt')
    expected = State(["ZN", "MCD", "P"], [(1, 1, 0), (3, 0, 2), (2, 1, 0), (1, 0, 1)])
    result = State.parse(data)
    assert result == expected


def test_step():
    data = utils.read_data(day_num, 'test01.txt')
    state = State.parse(data)
    expected = ["ZND", "MC", "P"]
    result = State.do_move9000(state.crates, state.moves[0])
    assert result == expected


def test_all_moves():
    data = utils.read_data(day_num, 'test01.txt')
    state = State.parse(data)
    expected = ["C", "M", "PDNZ"]
    result = state.all_moves9000()
    assert result == expected


def test_all_moves9001():
    data = utils.read_data(day_num, 'test01.txt')
    state = State.parse(data)
    expected = ["M", "C", "PZND"]
    result = state.all_moves9001()
    assert result == expected
