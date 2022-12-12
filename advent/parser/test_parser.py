from advent.parser.parser import P
import pytest


def test_one_letter():
    parser = P.char('!')
    input = '!'
    expected = '!'
    result = parser.parse(input).get()
    assert result == expected


def test_one_letter_longer():
    parser = P.char('!')
    input = '!!'
    expected = '!'
    result = parser.parse(input).get()
    assert result == expected


def test_one_string():
    parser = P.string('123')
    input = '12345'
    expected = '123'
    result = parser.parse(input).get()
    assert result == expected


def test_eof():
    parser = P.eof()
    input = ''
    result = parser.parse(input).get()
    assert result == ()

    input = '!'
    with pytest.raises(Exception):
        parser.parse(input).get()


def test_integer():
    parser = P.signed()
    input = '123456'
    expected = 123456
    result = parser.parse(input).get()
    assert result == expected


def test_signed_integer():
    parser = P.signed()
    input = '-123456'
    expected = -123456
    result = parser.parse(input).get()
    assert result == expected


def test_starting_zero():
    parser = P.unsigned()
    input = '0a'
    expected = 0
    result = parser.parse(input).get()
    assert result == expected

    input2 = '01'
    result2 = parser.parse(input2)
    assert result2.is_fail()


def test_between():
    parser = P.signed().between(P.char('<'), P.char('>'))
    input = '<-123456>'
    expected = -123456
    result = parser.parse(input).get()
    assert result == expected


def test_sep_by():
    parser = P.signed().sep_by(P.char(','))
    input = '2,3,5'
    expected = [[2, 3, 5], [2, 3], [2]]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_sep_by_lazy():
    parser = P.signed().sep_by_lazy(P.char(','))
    input = '2,3,5'
    expected = [[2], [2, 3], [2, 3, 5]]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_trim():
    parser = P.signed().trim()
    input = '1'
    expected = 1
    result = parser.parse(input).get()
    assert result == expected


def test_sep_by_trim():
    parser = P.signed().sep_by(P.char(',').trim()).trim()
    input = ' 1 , 1 , 2 , 3 , 5 , 8 , 13!'
    expected = [1, 1, 2, 3, 5, 8, 13]
    result = parser.parse(input).get()
    assert result == expected


def test_choice2():
    parser = P.choice(P.char('a'), P.unsigned(), P.string('hallo'))
    input = '1'
    expected = 1
    result = parser.parse(input).get()
    assert result == expected

    input = 'hallo'
    expected = 'hallo'
    result = parser.parse(input).get()
    assert result == expected


def test_seq():
    input = '1234'
    parser = P.seq(P.any_char(), P.any_char(), P.any_char(), P.any_char())
    expected = ('1', '2', '3', '4')
    result = parser.parse(input).get()
    assert result == expected


def test_seq_seq():
    input = '1,2,3,4'
    digit = P.char_func(lambda c: c.isdigit(), )
    parser = P.sep_seq(digit, digit, digit, digit, sep=P.char(','))

    expected = ('1', '2', '3', '4')
    result = parser.parse(input).get()
    assert result == expected


def test_not():
    input = 'a'
    parser = P.second(P.char('!').no_match(), P.char('a'))
    expected = 'a'
    result = parser.parse(input).get()
    assert result == expected

    input2 = '!'
    result2 = parser.parse(input2)
    assert result2.is_fail()


def test_multi():
    input = 'aa'
    parser = P.char('a').many()
    expected = [['a', 'a'], ['a'], []]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_either():
    input = 'aab'
    parser = P.either(
        P.seq(
            P.char('a').many(), P.string('b')), P.seq(
            P.string('a'), P.string('ab')))
    expected = [(['a', 'a'], 'b'), ('a', 'ab')]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_seq_eof():
    input = 'aa'
    parser = P.seq(P.char('a').many(), P.eof())
    expected = [(['a', 'a'], ())]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_optional():
    input = '12'
    parser = P.seq(P.char('1').optional(), P.unsigned())
    expected = [('1', 2), (None, 12)]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_choice():
    input = '1'
    parser = P.choice(P.char('1'), P.char('b'), P.unsigned())
    expected = ['1', 1]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_times_exact():
    input = 'aaa'
    parser = P.char('a').times(exact=2)
    expected = [['a', 'a']]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_times_min():
    input = 'aaa'
    parser = P.char('a').times(min=2)
    expected = [['a', 'a', 'a'], ['a', 'a']]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_times_max():
    input = 'aaa'
    parser = P.char('a').times(max=2)
    expected = [['a', 'a'], ['a'], []]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_some_lazy():
    input = 'aa'
    parser = P.char('a').some_lazy()
    expected = [['a'], ['a', 'a']]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_many_lazy():
    input = 'aa'
    parser = P.char('a').many_lazy()
    expected = [[], ['a'], ['a', 'a']]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_times_lazy_exact():
    input = 'aaa'
    parser = P.char('a').times_lazy(exact=2)
    expected = [['a', 'a']]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_times_lazy_min():
    input = 'aaa'
    parser = P.char('a').times_lazy(min=2)
    expected = [['a', 'a'], ['a', 'a', 'a']]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_times_lazy_max():
    input = 'aaa'
    parser = P.char('a').times_lazy(max=2)
    expected = [[], ['a'], ['a', 'a']]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_word():
    input = '123'
    parser = P.any_decimal().word()
    expected = ['123']
    result = list(parser.parse_multi(input))
    assert result == expected


def test_word2():
    input = '123a'
    parser = P.seq(P.any_decimal().word(), P.char('a'))
    expected = [('123', 'a')]
    result = list(parser.parse_multi(input))
    assert result == expected


def test_iterator_input():
    input = iter(['1', '2'])
    parser = P.unsigned().line().many()
    expected = [1, 2]
    result = parser.parse(input).get()
    assert result == expected


def test_iterator_trim_input():
    input = iter(['1 ', '2 '])
    parser = P.unsigned().trim().line().many()
    expected = [1, 2]
    result = parser.parse(input).get()
    assert result == expected
