from nose.tools import assert_raises
from nose.tools import eq_ as equal

from ripple import jsonrpc


def test_check_result_simple():
    response = dict([
        ('status', 'success'),
        ('foo', 'bar'),
    ])
    response = dict([
        ('result', response),
    ])

    @jsonrpc.check_result
    def _test(res):
        expect = dict([
            ('foo', 'bar')
        ])
        equal(res, expect)
    _test(response)


def test_check_result_no_result():
    response = dict([
        ('status', 'success'),
        ('foo', 'bar'),
    ])

    @jsonrpc.check_result
    def _test(res):
        raise AssertionError('Function should not have been called')
    with assert_raises(KeyError) as exc:
        _test(response)
    exc = exc.exception
    expect = 'The response did not return a "result" field'
    equal(exc.message, expect)


def test_check_result_no_status():
    response = dict([
        ('foo', 'bar'),
    ])
    response = dict([
        ('result', response),
    ])

    @jsonrpc.check_result
    def _test(res):
        raise AssertionError('Function should not have been called')
    with assert_raises(KeyError) as exc:
        _test(response)
    exc = exc.exception
    expect = 'The response did not return a "result.status" field'
    equal(exc.message, expect)


def test_check_result_error():
    response = dict([
        ('status', 'error'),
        ('error', 'foo_name'),
        ('error_code', 'foo_code'),
        ('error_message', 'foo_message'),
    ])
    response = dict([
        ('result', response),
    ])

    @jsonrpc.check_result
    def _test(res):
        raise AssertionError('Function should not have been called')
    with assert_raises(jsonrpc.RippleRPCError) as exc:
        _test(response)
    exc = exc.exception
    expect = 'foo_name, foo_code: foo_message'
    equal(str(exc), expect)
