from typing import *
from core.permissions import conf


def has_custom_permission(*args, **kwargs):
    name = kwargs.get("name")

    def decorator(func: Callable):
        return func
    #     def inner(*args, **kwargs):
    #         func(*args, **kwargs)
    #
    #     return inner
    #
    return decorator