import typing

ResultType = int | str | list[str]


class Day(typing.Protocol):
    day_num: int

    @staticmethod
    def part1(lines: typing.Iterator[str]) -> ResultType | None:
        ...

    @staticmethod
    def part2(lines: typing.Iterator[str]) -> ResultType | None:
        ...


def is_day(object: typing.Any) -> typing.TypeGuard[Day]:
    try:
        return (isinstance(object.day_num, int)
                and callable(object.part1) and callable(object.part2))
    except AttributeError:
        return False
