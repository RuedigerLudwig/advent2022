from advent.common import input

from .solution import day_num, parse_single_pair, PacketList, part1, part2


def test_part1():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 13
    result = part1(lines)
    assert result == expected


def test_part2():
    lines = input.read_lines(day_num, 'example01.txt')
    expected = 140
    result = part2(lines)
    assert result == expected


def test_parse_line():
    input = "[[4,4],4,4]"
    expected = PacketList([[4, 4], 4, 4])
    result = PacketList.parse(input)
    assert result == expected


def test_parse_pair():
    input = ["[1,1,3,1,1]", "[1,1,5,1,1]"]
    expected = PacketList([1, 1, 3, 1, 1]), PacketList([1, 1, 5, 1, 1])
    result = parse_single_pair(iter(input))
    assert result == expected


def test_compare1():
    left, right = PacketList([1, 1, 3, 1, 1]), PacketList([1, 1, 5, 1, 1])
    assert left < right


def test_compare3():
    left, right = PacketList([9]), PacketList([8, 7, 6])
    assert not left < right
