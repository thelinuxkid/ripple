from nose.tools import (
    assert_raises,
    assert_dict_equal,
    assert_tuple_equal,
)
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


def test_check_options_simple():
    @jsonrpc.check_options('ledger')
    def _test(*args, **kwargs):
        expect = ('foo', 'bar')
        assert_tuple_equal(args, expect)
        expect = dict([
            ('baz', 'qux'),
            ('ledger_hash', 'foo_ledger'),
        ])
        assert_dict_equal(kwargs, expect)
    _test('foo', 'bar', baz='qux', ledger_hash='foo_ledger')


def test_check_options_missing():
    @jsonrpc.check_options('ledger')
    def _test(*args, **kwargs):
        raise AssertionError('Function should not have been called')
    with assert_raises(ValueError) as exc:
        _test('foo', 'bar', baz='qux')
    exc = exc.exception
    expect = (
        'At least one option is needed: ledger_hash, ledger_index'
    )
    equal(str(exc), expect)


def test_check_options_many():
    @jsonrpc.check_options('ledger')
    def _test(*args, **kwargs):
        raise AssertionError('Function should not have been called')
    with assert_raises(ValueError) as exc:
        _test(
            'foo',
            'bar',
            baz='qux',
            ledger_hash='foo',
            ledger_index='bar',
        )
    exc = exc.exception
    expect = (
        'Only one option can be specified: ledger_hash, ledger_index'
    )
    equal(str(exc), expect)


def test_check_options_invalid():
    @jsonrpc.check_options('foo', 'ledger')
    def _test(*args, **kwargs):
        raise AssertionError('Function should not have been called')
    with assert_raises(ValueError) as exc:
        _test()
    exc = exc.exception
    expect = 'Invalid option set: foo'
    equal(str(exc), expect)


def test_check_options_empty():
    @jsonrpc.check_options()
    def _test(*args, **kwargs):
        raise AssertionError('Function should not have been called')
    with assert_raises(ValueError) as exc:
        _test()
    exc = exc.exception
    expect = 'At least one option set is needed: ledger'
    equal(str(exc), expect)


def test_check_options_multiple():
    jsonrpc.unique_options = dict([
        ('foo', ['foo_hash', 'foo_index']),
        ('bar', ['bar_hash', 'bar_index']),
    ])

    @jsonrpc.check_options('foo', 'bar')
    def _test(*args, **kwargs):
        raise AssertionError('Function should not have been called')
    with assert_raises(ValueError) as exc:
        _test(
            foo_hash='foo hash',
            bar_hash='bar hash',
            bar_index='bar index',
        )
    exc = exc.exception
    expect = 'Only one option can be specified: bar_hash, bar_index'
    equal(str(exc), expect)
