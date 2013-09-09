
from __future__ import nested_scopes

import functools

def ghetto_retry(count, exceptions=(Exception,)):
    """Ghetto retry attempts a function repetitively.

    Example usage:

    @ghetto_retry(3, exceptions=(FooError,))
    def function_that_may_throw_FooError():
        # ...

    Args:
        count - Maximum times to retry.
        exceptions - The types of exceptions to capture.
    """
    def _ghetto_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # I couldn't figure out this weirdness but this makes this work
            # Otherwise I get an UnboundLocalError
            __count = count
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    __count -= 1
                    if __count <= 0:
                        raise
        return wrapper
    return _ghetto_retry
