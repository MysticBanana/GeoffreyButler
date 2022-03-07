import functools

def exception_handler():
    """

    """
    def decorator(func):

        @functools.wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise e

        return inner
    return decorator