from abc import abstractmethod
from typing import Iterable, Iterator, Protocol, TypeVar


T = TypeVar('T', covariant=True)


class EofException(Exception):
    pass


class Provider(Iterator[T], Iterable[T], Protocol[T]):
    @abstractmethod
    def peek(self) -> T:
        ...

    @abstractmethod
    def get(self) -> T:
        ...

    @abstractmethod
    def finished(self) -> bool:
        ...

    def __next__(self) -> T:
        if self.finished():
            raise StopIteration()
        return self.get()

    def __iter__(self):
        return self
