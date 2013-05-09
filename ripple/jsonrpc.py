from functools import wraps


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
