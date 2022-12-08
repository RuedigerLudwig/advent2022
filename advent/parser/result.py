from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Never, TypeVar

S = TypeVar("S", covariant=True)
S1 = TypeVar("S1")
S2 = TypeVar("S2")
S3 = TypeVar("S3")


class Result(ABC, Generic[S]):
    @staticmethod
    def of(value: S1) -> Result[S1]:
        return Success(value)

    @staticmethod
    def fail(failure: str) -> Result[Any]:
        return Failure(failure)

    @abstractmethod
    def is_ok(self) -> bool:
        pass

    @abstractmethod
    def is_fail(self) -> bool:
        pass

    @abstractmethod
    def fmap(self, func: Callable[[S], S2]) -> Result[S2]:
        pass

    @abstractmethod
    def bind(self, func: Callable[[S], Result[S2]]) -> Result[S2]:
        pass

    @abstractmethod
    def get(self) -> S:
        pass

    @abstractmethod
    def get_or(self, default: S1) -> S | S1:
        pass

    @abstractmethod
    def get_or_else(self, default: Callable[[], S]) -> S:
        pass

    @abstractmethod
    def get_error(self) -> str:
        pass


class Success(Result[S]):
    def __init__(self, value: S):
        self.value = value

    def is_ok(self) -> bool:
        return True

    def is_fail(self) -> bool:
        return False

    def fmap(self, func: Callable[[S], S2]) -> Result[S2]:
        return Result.of(func(self.value))

    def bind(self, func: Callable[[S], Result[S2]]) -> Result[S2]:
        return func(self.value)

    def get(self) -> S:
        return self.value

    def get_or(self, default: S1) -> S | S1:
        return self.value

    def get_or_else(self, default: Callable[[], S]) -> S:
        return self.value

    def get_error(self) -> Never:
        raise Exception("No Error in Success Value")


class Failure(Result[Any]):
    def __init__(self, value: str):
        self.value = value

    def is_ok(self) -> bool:
        return False

    def is_fail(self) -> bool:
        return True

    def fmap(self, func: Callable[[Any], S2]) -> Result[S2]:
        return self

    def bind(self, func: Callable[[Any], Result[S2]]) -> Result[S2]:
        return self

    def get(self) -> Never:
        raise Exception("No value in Fail")

    def get_or(self, default: S1) -> S1:
        return default

    def get_or_else(self, default: Callable[[], S]) -> S:
        return default()

    def get_error(self) -> str:
        return self.value
