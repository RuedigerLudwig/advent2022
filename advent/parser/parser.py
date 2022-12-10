from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from itertools import chain
from typing import Any, Callable, Generic, Iterator, Self, TypeVar, overload
import unicodedata

from .result import Result

T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')
TR = TypeVar('TR')


@dataclass(slots=True, frozen=True)
class ParserInput:
    input: str
    start: int

    def step(self) -> tuple[Self, str]:
        if self.start >= len(self.input):
            raise Exception("Already at End of Input")

        return ParserInput(self.input, self.start + 1), self.input[self.start]

    def has_data(self) -> bool:
        return self.start < len(self.input)

    def __repr__(self) -> str:
        if self.start == 0:
            return f'->[{self.input}]'
        if self.start >= len(self.input):
            return f'{self.input}'
        if self.start < 3:
            return f'{self.input[0:self.start-1]}->[{self.input[self.start:]}]'
        return f'{self.input[self.start-3:self.start-1]}->[{self.input[self.start:]}]'


ParserResult = Iterator[tuple[ParserInput, T]]
ParserFunc = Callable[[ParserInput], ParserResult[T]]


class P(Generic[T]):
    def __init__(self, func: ParserFunc[T]):
        self.func = func

    def parse(self, s: str, i: int = 0) -> Result[T]:
        all_results = self.func(ParserInput(s, i))
        try:
            _, result = next(all_results)
            return Result.of(result)
        except StopIteration:
            return Result.fail("No result")

    def parse_multi(self, s: str, i: int = 0) -> Iterator[T]:
        return (v for _, v in self.func(ParserInput(s, i)))

    @staticmethod
    def pure(value: T) -> P[T]:
        return P(lambda pp: iter([(pp, value)]))

    @staticmethod
    def fail() -> P[Any]:
        return P(lambda _: iter([]))

    @staticmethod
    def _fix(p1: Callable[[P[Any]], P[T]]) -> P[T]:
        """ Not really nice helper function, but it works"""
        return [p._forward(q.func) for p in [P(None)] for q in [p1(p)]][0]  # type: ignore

    def _forward(self, func: ParserFunc[T]) -> Self:
        self.func = func
        return self

    def bind(self, bind_func: Callable[[T], P[TR]]) -> P[TR]:
        def inner(parserPos: ParserInput) -> ParserResult[TR]:
            return (r for rs in (bind_func(v).func(pp)
                    for pp, v in self.func(parserPos)) for r in rs)
        return P(inner)

    def fmap(self, map_func: Callable[[T], TR]) -> P[TR]:
        def inner(parserPos: ParserInput) -> ParserResult[TR]:
            return ((pp, map_func(v)) for pp, v in self.func(parserPos))
        return P(inner)

    def safe_fmap(self, map_func: Callable[[T], TR]) -> P[TR]:
        def inner(parserPos: ParserInput) -> ParserResult[TR]:
            for pp, v in self.func(parserPos):
                try:
                    yield pp, map_func(v)
                except Exception:
                    pass

        return P(inner)

    def replace(self, value: TR) -> P[TR]:
        return self.fmap(lambda _: value)

    def unit(self) -> P[tuple[()]]:
        return self.fmap(lambda _: ())

    def apply(self, p2: P[Callable[[T], TR]]) -> P[TR]:
        return self.bind(lambda x: p2.bind(lambda y: P.pure(y(x))))

    def between(self, pre: P[Any], post: P[Any]) -> P[T]:
        return P.map3(pre, self, post, lambda _1, v, _2: v)

    def surround(self, other: P[Any]) -> P[T]:
        return P.map3(other, self, other, lambda _1, v, _2: v)

    def some_lazy(self) -> P[list[T]]:
        return P._fix(lambda p: self.bind(
            lambda x: P.either(P.pure([]), p).fmap(lambda ys: [x] + ys)))

    def some(self) -> P[list[T]]:
        return P._fix(lambda p: self.bind(
            lambda x: P.either(p, P.pure([])).fmap(lambda ys: [x] + ys)))

    def many(self) -> P[list[T]]:
        return P.either(self.some(), P.pure([]))

    def many_lazy(self) -> P[list[T]]:
        return P.either(P.pure([]), self.some_lazy())

    def satisfies(self, pred: Callable[[T], bool]) -> P[T]:
        return self.bind(lambda v: P.pure(v) if pred(v) else P.fail())

    def optional(self) -> P[T | None]:
        return P.either(self, P.pure(None))

    def optional_lazy(self) -> P[T | None]:
        return P.either(P.pure(None), self)

    def times(self, *, max: int | None = None, min: int | None = None,
              exact: int | None = None) -> P[list[T]]:
        match (exact, min, max):
            case (int(e), None, None):
                return self.many().satisfies(lambda lst: len(lst) == e)
            case (None, int(mn), None):
                return self.many().satisfies(lambda lst: len(lst) >= mn)
            case (None, None, int(mx)):
                return self.many().satisfies(lambda lst: len(lst) <= mx)
            case _:
                raise Exception("Choose exactly one of exact, min or max")

    def times_lazy(self, *, max: int | None = None, min: int | None = None,
                   exact: int | None = None) -> P[list[T]]:
        match (exact, min, max):
            case (int(e), None, None):
                return self.many_lazy().satisfies(lambda lst: len(lst) == e)
            case (None, int(mn), None):
                return self.many_lazy().satisfies(lambda lst: len(lst) >= mn)
            case (None, None, int(mx)):
                return self.many_lazy().satisfies(lambda lst: len(lst) <= mx)
            case _:
                raise Exception("Choose exactly one of exact, min or max")

    def sep_by(self, sep: P[Any]) -> P[list[T]]:
        return P.map2(self, P.second(sep, self).many(), lambda f, r: [f] + r)

    @staticmethod
    def first(p1: P[T1], p2: P[Any]) -> P[T1]:
        return P.map2(p1, p2, lambda v1, _: v1)

    @staticmethod
    def second(p1: P[Any], p2: P[T2]) -> P[T2]:
        return p1.bind(lambda _: p2)

    @staticmethod
    def no_match(p: P[Any]) -> P[tuple[()]]:
        def inner(parserPos: ParserInput) -> ParserResult[tuple[()]]:
            result = p.func(parserPos)
            try:
                next(result)
                # Silently yields nothing so is an empty Generator
            except StopIteration:
                yield (parserPos, ())

        return P(inner)

    @staticmethod
    def map2(p1: P[T1], p2: P[T2], func: Callable[[T1, T2], TR]) -> P[TR]:
        return p1.bind(lambda v1: p2.fmap(lambda v2: func(v1, v2)))

    @staticmethod
    def map3(p1: P[T1], p2: P[T2], p3: P[T3], func: Callable[[T1, T2, T3], TR]) -> P[TR]:
        return p1.bind(
            lambda v1: p2.bind(
                lambda v2: p3.fmap(
                    lambda v3: func(v1, v2, v3))))

    @staticmethod
    def map4(p1: P[T1], p2: P[T2], p3: P[T3], p4: P[T4],
             func: Callable[[T1, T2, T3, T4], TR]) -> P[TR]:
        return p1.bind(
            lambda v1: p2.bind(
                lambda v2: p3.bind(
                    lambda v3: p4.fmap(
                        lambda v4: func(v1, v2, v3, v4)))))

    @staticmethod
    def map5(p1: P[T1], p2: P[T2], p3: P[T3], p4: P[T4], p5: P[T5],
             func: Callable[[T1, T2, T3, T4, T5], TR]) -> P[TR]:
        return p1.bind(
            lambda v1: p2.bind(
                lambda v2: p3.bind(
                    lambda v3: p4.bind(
                        lambda v4: p5.fmap(
                            lambda v5: func(v1, v2, v3, v4, v5))))))

    @staticmethod
    @overload
    def seq(p1: P[T1], p2: P[T2], /) -> P[tuple[T1, T2]]:
        ...

    @staticmethod
    @overload
    def seq(p1: P[T1], p2: P[T2], p3: P[T3], /) -> P[tuple[T1, T2, T3]]:
        ...

    @staticmethod
    @overload
    def seq(p1: P[T1], p2: P[T2], p3: P[T3], p4: P[T4], /) -> P[tuple[T1, T2, T3, T4]]:
        ...

    @staticmethod
    @overload
    def seq(p1: P[T1], p2: P[T2], p3: P[T3], p4: P[T4],
            p5: P[T5], /) -> P[tuple[T1, T2, T3, T4, T5]]:
        ...

    @staticmethod
    def seq(*ps: P[Any]) -> P[tuple[Any, ...]]:
        return reduce(lambda p, x: x.bind(
            lambda a: p.fmap(lambda b: chain([a], b))),
            list(ps)[::-1], P.pure(iter([]))).fmap(tuple)

    @staticmethod
    @overload
    def sep_seq(p1: P[T1], p2: P[T2], /, *, sep: P[Any]) -> P[tuple[T1, T2]]:
        ...

    @staticmethod
    @overload
    def sep_seq(p1: P[T1], p2: P[T2], p3: P[T3], /, *, sep: P[Any]) -> P[tuple[T1, T2, T3]]:
        ...

    @staticmethod
    @overload
    def sep_seq(p1: P[T1], p2: P[T2], p3: P[T3], p4: P[T4], /,
                *, sep: P[Any]) -> P[tuple[T1, T2, T3, T4]]:
        ...

    @staticmethod
    @overload
    def sep_seq(p1: P[T1], p2: P[T2], p3: P[T3], p4: P[T4],
                p5: P[T5], /, *, sep: P[Any]) -> P[tuple[T1, T2, T3, T4, T5]]:
        ...

    @staticmethod
    def sep_seq(*ps: P[Any], sep: P[Any]) -> P[tuple[Any, ...]]:
        first, *rest = list(ps)
        return P.map2(first,
                      reduce(lambda p, x: P.second(sep, x.bind(
                          lambda a: p.fmap(lambda b: chain([a], b)))),
                          rest[::-1], P.pure(iter([]))),
                      lambda f, r: (f,) + tuple(r))

    @staticmethod
    def either(p1: P[T1], p2: P[T2], /) -> P[T1 | T2]:
        def inner(parserPos: ParserInput):
            yield from p1.func(parserPos)
            yield from p2.func(parserPos)

        return P(inner)

    @staticmethod
    @overload
    def choice(p1: P[T1], p2: P[T2], p3: P[T3], /) -> P[T1 | T2 | T3]:
        ...

    @staticmethod
    @overload
    def choice(p1: P[T1], p2: P[T2], p3: P[T3], p4: P[T4], /) -> P[T1 | T2 | T3 | T4]:
        ...

    @staticmethod
    @overload
    def choice(p1: P[T1], p2: P[T2], p3: P[T3], p4: P[T4],
               p5: P[T5], /) -> P[T1 | T2 | T3 | T4 | T5]:
        ...

    @staticmethod
    def choice(*ps: P[Any]) -> P[Any]:
        def inner(parserPos: ParserInput) -> Iterator[Any]:
            for p in ps:
                yield from p.func(parserPos)
        return P(inner)

    @staticmethod
    def choice2(*ps: P[T]) -> P[T]:
        return P.choice(*ps)

    @staticmethod
    def one_char() -> P[str]:
        def inner(parserPos: ParserInput) -> ParserResult[str]:
            if parserPos.has_data():
                yield parserPos.step()
        return P(inner)

    @staticmethod
    def eof() -> P[tuple[()]]:
        def inner(parserPos: ParserInput) -> ParserResult[tuple[()]]:
            if not parserPos.has_data():
                yield parserPos, ()
        return P(inner)

    @staticmethod
    def char_func(cmp: Callable[[str], bool]) -> P[str]:
        return P.one_char().satisfies(cmp)

    @staticmethod
    def is_char(cmp: str) -> P[str]:
        return P.char_func(lambda c: c == cmp)

    @staticmethod
    def is_not_char(s: str) -> P[tuple[()]]:
        return P.no_match(P.is_char(s))

    @staticmethod
    def string(s: str) -> P[str]:
        return P.seq(*map(P.is_char, s)).replace(s)

    @staticmethod
    def one_of(s: str) -> P[str]:
        return P.char_func(lambda c: c in s)

    @staticmethod
    def any_decimal() -> P[str]:
        return P.char_func(lambda c: c.isdecimal())

    @staticmethod
    def is_decimal(num: int) -> P[str]:
        return P.any_decimal().satisfies(lambda c: unicodedata.decimal(c) == num)

    @staticmethod
    def is_not_decimal(num: int) -> P[str]:
        return P.any_decimal().satisfies(lambda c: unicodedata.decimal(c) != num)

    @staticmethod
    def lower() -> P[str]:
        return P.char_func(lambda c: c.islower())

    @staticmethod
    def upper() -> P[str]:
        return P.char_func(lambda c: c.isupper())

    @staticmethod
    def space() -> P[str]:
        return P.char_func(lambda c: c.isspace())

    @staticmethod
    def word(p1: P[str]) -> P[str]:
        return P.first(p1.many().fmap(lambda cs: ''.join(cs)), P.no_match(p1))

    @staticmethod
    def unsigned() -> P[int]:
        return P.either(P.first(P.is_decimal(0), P.no_match(P.any_decimal())),
                        P.map2(P.is_not_decimal(0), P.word(P.any_decimal()),
                               lambda f, s: f + s)
                        ).fmap(int)

    @staticmethod
    def signed() -> P[int]:
        return P.map2(P.one_of('+-').optional(), P.unsigned(),
                      lambda sign, num: num if sign != '-' else -num)

    def in_parens(self) -> P[T]:
        return self.between(P.is_char('('), P.is_char(')'))

    def in_angles(self) -> P[T]:
        return self.between(P.is_char('<'), P.is_char('>'))

    def in_brackets(self) -> P[T]:
        return self.between(P.is_char('['), P.is_char(']'))

    def in_curleys(self) -> P[T]:
        return self.between(P.is_char('{'), P.is_char('}'))

    def trim_left(self) -> P[T]:
        return P.second(WHITE_SPACE, self)

    def trim_right(self) -> P[T]:
        return P.first(self, WHITE_SPACE)

    def trim(self) -> P[T]:
        return self.surround(WHITE_SPACE)


WHITE_SPACE: P[tuple[()]] = P.space().many().unit()
SEP_SPACE: P[tuple[()]] = P.space().some().unit()
