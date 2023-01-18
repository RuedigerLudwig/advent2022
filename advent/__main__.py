from importlib import import_module
import time
import sys
from advent.common import input
from advent.days.template import Day, ResultType, is_day


def output(day: int, part: int, result: ResultType | None, delta: float) -> None:
    match result:
        case int(value):
            print(f'Day {day:02} Part {part}: {value} ({delta:0.3}s)')
        case str(value):
            print(f'Day {day:02} Part {part}: {value} ({delta:0.3}s)')
        case list(value):
            print(f'Day {day:02} Part {part}: {value[0]} ({delta:0.3}s)')
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


def run(day: Day, part: int) -> float:
    data = input.read_lines(day.day_num, 'input.txt')
    t0 = time.time()
    match part:
        case 1: result = day.part1(data)
        case 2: result = day.part2(data)
        case _: raise Exception(f'Unknown part {part}')
    t1 = time.time()
    delta = t1 - t0
    output(day.day_num, part, result, delta)
    return delta


def run_from_string(day_str: str) -> float:
    match day_str.split('/'):
        case [d]:
            day_num = int(d)
            day = get_day(day_num)

            if day_num == day.day_num:
                p1 = run(day, 1)
                p2 = run(day, 2)
                return p1 + p2

            assert False, "We should never get here"

        case [d, p]:
            day_num = int(d)
            day = get_day(day_num)

            if day_num == day.day_num:
                part = int(p)
                return run(day, part)

            assert False, "We should never get here"

        case _:
            raise Exception(f'{day_str} is not a valid day description')


def main() -> None:
    print()
    time = 0.0
    match sys.argv:
        case [_]:
            try:
                for day_num in range(1, 25):
                    day = get_day(day_num)
                    if day_num == day.day_num:
                        time += run(day, 1)
                        time += run(day, 2)
            except ModuleNotFoundError:
                pass

        case [_, argument]:
            time += run_from_string(argument)

        case _:
            raise Exception(f'Usage: python {sys.argv[0]} [day[/part]]')

    print(f"\nTotal time: {time:0.3}s")


if __name__ == '__main__':
    main()
