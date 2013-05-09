import sys

import mock

from datetime import datetime

from dateutil import tz
from nose.tools import assert_raises
from nose.tools import eq_ as equal

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
    equal(exc.message, expect)


def test_drop_string():
    value = 'foo'
    with assert_raises(ValueError) as exc:
        jsonformat.drop(value)
    exc = exc.exception
    expect = 'Value must be a positive integer: foo'
    equal(exc.message, expect)


def test_drop_negative():
    value = '-1'
    with assert_raises(ValueError) as exc:
        jsonformat.drop(value)
    exc = exc.exception
    expect = 'Value must be a positive integer: -1'
    equal(exc.message, expect)


def test_drop_max():
    value = '100000000000'
    res = jsonformat.drop(value)
    equal(res, 100000000000L)


def test_drop_sys_max():
    max_value = sys.maxint + 1
    value = str(max_value)
    res = jsonformat.drop(value)
    equal(res, max_value)


def test_drop_sys_min():
    min_value = -sys.maxint - 2
    value = str(min_value)
    with assert_raises(ValueError) as exc:
        jsonformat.drop(value)
    exc = exc.exception
    expect = 'Value must be a positive integer: {min_value}'.format(
        min_value=min_value,
    )
    equal(exc.message, expect)


def test_totime_simple():
    dt = datetime(2013, 5, 9, 0, 55, 24, tzinfo=tz.tzutc())
    res = jsonformat.totime(dt)
    expect = 421376124
    equal(res, expect)


def test_totime_earlier():
    dt = datetime(1999, 5, 9, 0, 55, 24, tzinfo=tz.tzutc())
    with assert_raises(ValueError) as exc:
        jsonformat.totime(dt)
    exc = exc.exception
    expect = (
        'Value cannot be earlier than 2000-01-01T00:00:00+00:00: '
        '1999-05-09T00:55:24+00:00'
    )
    equal(exc.message, expect)


def test_totime_notz():
    dt = datetime(2013, 5, 9, 0, 55, 24)
    with assert_raises(ValueError) as exc:
        jsonformat.totime(dt)
    exc = exc.exception
    expect = (
        'Value must contain timezone information: 2013-05-09T00:55:24'
    )
    equal(exc.message, expect)


def test_fromtime_simple():
    res = jsonformat.fromtime(421376124)
    expect = datetime(2013, 5, 9, 0, 55, 24, tzinfo=tz.tzutc())
    equal(res, expect)


def test_utc_from_iso_simple():
    dt = jsonformat.utc_from_iso('2011-11-16T18:36:06.795119-08:00')
    expect = datetime(2011, 11, 17, 2, 36, 06, 795119, tz.tzutc())
    equal(dt, expect)


def test_utc_from_iso_utc():
    dt = jsonformat.utc_from_iso('2011-10-12T19:55:58.345128+0000')
    expect = datetime(2011, 10, 12, 19, 55, 58, 345128, tz.tzutc())
    equal(dt, expect)


@mock.patch('dateutil.tz.tzlocal')
def test_utc_from_iso_local(fake_local):
    fake_local.return_value = tz.tzoffset(None, -10800)
    dt = jsonformat.utc_from_iso(
        '2011-11-16T18:36:06.795119',
        assume_local=True,
    )
    expect = datetime(2011, 11, 16, 21, 36, 06, 795119, tz.tzutc())
    equal(dt, expect)


def test_utc_from_empty():
    with assert_raises(ValueError) as exc:
        jsonformat.utc_from_iso('')
    exc = exc.exception
    expect = 'Value cannot be empty string'
    equal(exc.message, expect)


def test_utc_from_notz():
    with assert_raises(ValueError) as exc:
        jsonformat.utc_from_iso('2013-05-09T00:55:24')
    exc = exc.exception
    expect = (
        'Value must contain timezone information: 2013-05-09T00:55:24'
    )
    equal(exc.message, expect)
