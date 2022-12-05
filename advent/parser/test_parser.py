from advent.parser.parser import P
import pytest


def test_one_letter():
    parser = P.is_char('!')
    input = '!'
    expected = '!'
    result = parser.parse(input).get()
    assert result == expected


def test_one_letter_longer():
    parser = P.is_char('!')
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
    parser = P.signed().between(P.is_char('<'), P.is_char('>'))
    input = '<-123456>'
    expected = -123456
    result = parser.parse(input).get()
    assert result == expected


def test_sep_by():
    parser = P.signed().sep_by(P.is_char(','))
    input = '1,1,2,3,5,8,13'
    expected = [1, 1, 2, 3, 5, 8, 13]
    result = parser.parse(input).get()
    assert result == expected


def test_trim():
    parser = P.signed().trim()
    input = '1'
    expected = 1
    result = parser.parse(input).get()
    assert result == expected


def test_sep_by_trim():
    parser = P.signed().sep_by(P.is_char(',').trim()).trim()
    input = ' 1 , 1 , 2 , 3 , 5 , 8 , 13!'
    expected = [1, 1, 2, 3, 5, 8, 13]
    result = parser.parse(input).get()
    assert result == expected


def test_choice2():
    parser = P.choice(P.is_char('a'), P.unsigned(), P.string('hallo'))
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
    digit = P.char_by_func(lambda c: c.isdigit(), "")
    parser = P.sep_seq(digit, digit, digit, digit, sep=P.is_char(','))

    expected = ('1', '2', '3', '4')
    result = parser.parse(input).get()
    assert result == expected


def test_not():
    input = 'a'
    parser = P.snd(P.no_match(P.is_char('!'), 'found !'), P.is_char('a'))
    expected = 'a'
    result = parser.parse(input).get()
    assert result == expected

    input2 = '!'
    result2 = parser.parse(input2)
    assert result2.is_fail()
