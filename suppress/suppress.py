from functools import wraps


class suppress:
    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._caught_exception(exc_val):
            self.exception = exc_val
            self.traceback = exc_tb
            return True

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return wrapper

    def _caught_exception(self, exc_val):
        return any(isinstance(exc_val, exc) for exc in self.exceptions)
