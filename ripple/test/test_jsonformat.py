import sys

from datetime import datetime

from dateutil import tz
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

def test_totime_simple():
    dt = datetime(2013, 5, 9, 0, 55, 24, tzinfo=tz.tzutc())
    res = jsonformat.totime(dt)
    expect = 421376124
    assert res == expect

def test_totime_earlier():
    dt = datetime(1999, 5, 9, 0, 55, 24, tzinfo=tz.tzutc())
    with assert_raises(ValueError) as exc:
        jsonformat.totime(dt)
    exc = exc.exception
    expect = (
        'Value cannot be earlier than 2000-01-01T00:00:00+00:00: '
        '1999-05-09T00:55:24+00:00'
    )
    assert exc.message == expect

def test_totime_notz():
    dt = datetime(2013, 5, 9, 0, 55, 24)
    with assert_raises(ValueError) as exc:
        jsonformat.totime(dt)
    exc = exc.exception
    expect = (
        'Value must contain timezone information: 2013-05-09T00:55:24'
    )
    assert exc.message == expect

def test_fromtime_simple():
    res = jsonformat.fromtime(421376124)
    expect = datetime(2013, 5, 9, 0, 55, 24, tzinfo=tz.tzutc())
    assert res == expect
