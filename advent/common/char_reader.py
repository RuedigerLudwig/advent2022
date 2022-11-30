from advent.common.provider import EofException
from .char_provider import CharProvider


class ReaderException(Exception):
    pass


class CharReader:
    @staticmethod
    def read_word(provider: CharProvider, word: str) -> str:
        result = ''
        for expected_char in word:
            try:
                char = provider.get()
                if char == expected_char:
                    result += char
                else:
                    raise ReaderException(f'Expected {word} but received {result}{char}')
            except EofException:
                raise ReaderException(f'Expected {word} but received {result}[EOF]')

        return word

    @staticmethod
    def read_unsigned_int(provider: CharProvider) -> int:
        if not provider.peek().isdigit():
            raise ReaderException('Expected unsigned int')

        number = 0
        while not provider.finished() and provider.peek().isdigit():
            number = number * 10 + int(provider.get())
        return number
