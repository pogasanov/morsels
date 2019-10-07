from dataclasses import dataclass
from functools import wraps
from typing import Any, Union


@dataclass
class Call:
    args: tuple
    kwargs: dict
    return_value: Any
    exception: Union[Exception, None] = None


NO_RETURN = object


def record_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            wrapper.calls.append(Call(args, kwargs, NO_RETURN, e))
            raise e

        wrapper.calls.append(Call(args, kwargs, result))
        return result

    wrapper.calls = []
    wrapper.call_count = 0
    return wrapper
