from advent.common import input

from .solution import CaveMap, FlooredCave, BottomLessCave, day_num, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 24
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'test01.txt')
    expected = 93
    result = part2(lines)
    assert result == expected


def test_parse_line():
    input = "98,4 -> 498,6 -> 496,6"
    expected = [(98, 4), (498, 6), (496, 6)]
    result = CaveMap.parse_rock_path(input)
    assert result == expected


def test_get_path():
    from_pos = 498, 4
    to_pos = 498, 6
    expected = [(498, 5), (498, 6)]
    result = list(CaveMap.get_path(from_pos, to_pos))
    assert result == expected


def test_get_path2():
    from_pos = 498, 6
    to_pos = 496, 6
    expected = [(497, 6), (496, 6)]
    result = list(CaveMap.get_path(from_pos, to_pos))
    assert result == expected


def test_parser_test():
    lines = input.read_lines(day_num, 'test01.txt')
    cave = BottomLessCave.create(lines)
    assert cave.cave_map.max_depths == 9


def test_drip():
    lines = input.read_lines(day_num, 'test01.txt')
    cave = BottomLessCave.create(lines)
    result = cave.drip()
    assert result is True
    assert cave.cave_map.is_filled((500, 8))


def test_drip2():
    lines = input.read_lines(day_num, 'test01.txt')
    cave = BottomLessCave.create(lines)
    cave.drip()
    cave.drip()
    assert cave.cave_map.is_filled((499, 8))


def test_drip_forever():
    lines = input.read_lines(day_num, 'test01.txt')
    cave = BottomLessCave.create(lines)
    result = cave.drip_till_forever()
    expected = 24
    assert result == expected


def test_drip_forever2():
    lines = input.read_lines(day_num, 'test01.txt')
    cave = FlooredCave.create(lines, floor=2)
    result = cave.drip_till_full()
    expected = 93
    assert result == expected
