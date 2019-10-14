from dataclasses import dataclass
from functools import wraps
from typing import Any, Optional

NO_RETURN = object()


@dataclass
class Call:
    args: tuple
    kwargs: dict
    return_value: Any = NO_RETURN
    exception: Optional[Exception] = None


def record_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1

        try:
            result = func(*args, **kwargs)
        except Exception as e:
            wrapper.calls.append(Call(args, kwargs, exception=e))
            raise e

        wrapper.calls.append(Call(args, kwargs, return_value=result))
        return result

    wrapper.calls = []
    wrapper.call_count = 0
    return wrapper
