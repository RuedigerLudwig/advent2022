import sys
from importlib import import_module

from advent.common import input
from advent.days.template import Day, ResultType, is_day


def output(day: int, part: int, result: ResultType | None) -> None:
    match result:
        case int(value):
            print('Day {0:02} Part {1}: {2}'.format(day, part, value))
        case str(value):
            print('Day {0:02} Part {1}: {2}'.format(day, part, value))
        case list(value):
            print('Day {0:02} Part {1}: {2}'.format(day, part, value[0]))
            for line in value[1:]:
                print(f'               {line}')
        case None:
            print('Day {0:02} Part {1}: (No Result)'.format(day, part))
        case _:
            print('Day {0:02} Part {1}: (Unknown result type)'.format(day, part))


def get_day(day_num: int) -> Day:
    day_module = import_module('advent.days.day{0:02}.solution'.format(day_num))
    if not is_day(day_module):
        raise Exception(f'Not a valid day: {day_num}')

    return day_module


def run(day: Day, part: int) -> None:
    data = input.read_lines(day.day_num, 'input.txt')
    match part:
        case 1: output(day.day_num, 1, day.part1(data))
        case 2: output(day.day_num, 2, day.part2(data))
        case _: raise Exception(f'Unknown part {part}')


def run_from_string(day_str: str) -> None:
    match day_str.split('/'):
        case [d]:
            day_num = int(d)
            day = get_day(day_num)

            if day_num == day.day_num:
                run(day, 1)
                run(day, 2)

        case [d, p]:
            day_num = int(d)
            day = get_day(day_num)

            if day_num == day.day_num:
                part = int(p)
                run(day, part)

        case _:
            raise Exception(f'{day_str} is not a valid day description')


def main() -> None:
    match sys.argv:
        case [_]:
            try:
                for day_num in range(1, 25):
                    day = get_day(day_num)
                    if day_num == day.day_num:
                        run(day, 1)
                        run(day, 2)
            except ModuleNotFoundError:
                pass

        case [_, argument]:
            run_from_string(argument)

        case _:
            raise Exception(f'Usage: python {sys.argv[0]} [day[/part]]')


if __name__ == '__main__':
    main()
