from advent.common import input

from .solution import day_num, part1, part2, Directory


def test_part1():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 95437
    result = part1(data)
    assert result == expected


def test_part2():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 24933642
    result = part2(data)
    assert result == expected


def test_size():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 48381165
    directory = Directory.parse(data)
    result = directory.get_size()
    assert result == expected


def test_maxed_size():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 95437
    directory = Directory.parse(data)
    result = directory.get_maxed_size(100_000)
    assert result == expected


def test_find_to_delete():
    data = input.read_lines(day_num, 'example01.txt')
    expected = 24933642
    directory = Directory.parse(data)
    result = directory.get_min_delete_size(70_000_000, 30_000_000)
    assert result == expected
