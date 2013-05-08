import sys

from nose.tools import assert_raises

from ripple import jsonformat

def test_drop_simple():
    value = '1'
    res = jsonformat.drop(value)
    assert res == 1

def test_drop_float():
    value = '1.0'
    with assert_raises(ValueError) as exc:
        jsonformat.drop(value)
    exc = exc.exception
    expect = 'Value must be a positive integer: 1.0'
    assert exc.message == expect

def test_drop_string():
    value = 'foo'
    with assert_raises(ValueError) as exc:
        jsonformat.drop(value)
    exc = exc.exception
    expect = 'Value must be a positive integer: foo'
    assert exc.message == expect

def test_drop_negative():
    value = '-1'
    with assert_raises(ValueError) as exc:
        jsonformat.drop(value)
    exc = exc.exception
    expect = 'Value must be a positive integer: -1'
    assert exc.message == expect

def test_drop_max():
    value = '100000000000'
    res = jsonformat.drop(value)
    assert res == 100000000000L

def test_drop_sys_max():
    max_value = sys.maxint + 1
    value = str(max_value)
    res = jsonformat.drop(value)
    assert res == max_value

def test_drop_sys_min():
    min_value = -sys.maxint - 2
    value = str(min_value)
    with assert_raises(ValueError) as exc:
        jsonformat.drop(value)
    exc = exc.exception
    expect = 'Value must be a positive integer: {min_value}'.format(
        min_value=min_value,
    )
    assert exc.message == expect
