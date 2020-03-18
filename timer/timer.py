from statistics import mean, median
from time import perf_counter


class Timer:
    def __init__(self, func=None):
        self.runs = []
        self.func = func

    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = perf_counter() - self.start
        self.runs.append(self.elapsed)
        self.mean = mean(self.runs)
        self.median = median(self.runs)
        self.min = min(self.runs)
        self.max = max(self.runs)

    def __call__(self, *args, **kwargs):
        with self:
            return self.func(*args, **kwargs)
