from functools import wraps

unique_options = dict([
    ('ledger', ['ledger_hash', 'ledger_index']),
])


class RippleRPCError(Exception):
    """"
    An error in an RPC response.
    """
    def __init__(self, name, code, message):
        self.name = name
        self.code = code
        self.message = message

    def __unicode__(self):
        msg = '{name}, {code}: {message}'.format(
            name=self.name,
            code=self.code,
            message=self.message,
        )
        return msg

    def __str__(self):
        return unicode(self)


def check_result(fn):
    """"
    Return the result in the response. If the response contains an
    error then raise an exception of type RippleRPCError containing
    the error information.
    """
    @wraps(fn)
    def wrapper(res):
        result = res.pop('result', None)
        if not result:
            raise KeyError(
                'The response did not return a "result" field'
            )
        status = result.pop('status', None)
        if not status:
            raise KeyError(
                'The response did not return a "result.status" field'
            )
        if status == 'error':
            raise RippleRPCError(
                name=result['error'],
                code=result['error_code'],
                message=result['error_message']
            )
        return fn(result)
    return wrapper


def check_options(*options):
    """
    Raise if the request contains more than one option in an option
    set. For example, a request should only contain one of ledger_hash
    or ledger_index.
    """
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not options:
                raise ValueError(
                    'At least one option set is needed: '
                    '{need}'.format(
                        need=', '.join(unique_options.keys())
                    )
                )
            check = [
                v for (k, v) in unique_options.items()
                if k in options
            ]
            if len(options) != len(check):
                diff = set(options) - set(unique_options.keys())
                raise ValueError(
                    'Invalid option set: {options}'.format(
                        options=', '.join(diff)
                    )
                )
            for unique in check:
                found = [
                    k for k in kwargs.keys() if k in unique
                ]
                if not found:
                    raise ValueError(
                        'At least one option is needed: {need}'.format(
                            need=', '.join(unique)
                        )
                    )
                if len(found) > 1:
                    raise ValueError(
                        'Only one option can be specified: '
                        '{need}'.format(
                            need=', '.join(unique),
                        )
                    )
            return fn(*args, **kwargs)
        return wrapped
    return wrapper
