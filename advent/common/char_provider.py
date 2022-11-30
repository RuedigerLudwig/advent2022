from typing import Iterable, Iterator

from .provider import EofException, Provider


class CharProvider(Provider[str]):
    data: Iterator[str]

    def __init__(self, data: Iterator[str] | Iterable[str]) -> None:
        if isinstance(data, Iterator):
            self.data = data
        else:
            self.data = iter(data)
        self.peeked: list[str] = []

    def _ensure_next(self) -> str:
        if not self.peeked:
            try:
                self.peeked = [next(self.data)]
            except StopIteration:
                raise EofException() from None
        return self.peeked[0]

    def peek(self) -> str:
        return self._ensure_next()

    def get(self) -> str:
        result = self._ensure_next()
        self.peeked = self.peeked[1:]
        return result

    def finished(self) -> bool:
        try:
            self._ensure_next()
            return False
        except EofException:
            return True
