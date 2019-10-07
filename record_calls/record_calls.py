from dataclasses import dataclass
from functools import wraps


@dataclass
class Call:
    args: tuple
    kwargs: dict
    return_value: any
    exception: any


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

        wrapper.calls.append(Call(args, kwargs, result, None))
        return result

    wrapper.calls = []
    wrapper.call_count = 0
    return wrapper
