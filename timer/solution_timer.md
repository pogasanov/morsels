# Solution: Timer

Hiya,

If you haven't attempted to solve Timer yet, close this email and go do that now before reading on. If you have attempted solving Timer, read on...

This week you needed to write a context manager that would record how long a block of code ran.

Here's one way to do this:

    from time import time

    class Timer:

        """Context manager to time a code block."""

        def __enter__(self):
            self.start = time()
            return self

        def __exit__(self, *args):
            self.end = time()
            self.elapsed = self.end - self.start

We're storing the `start` time when the `with` block is entered and then computing the `end` time after it exits and using that to calculate the `elapsed` time. We need to return `self` from our `__enter__` method so that our context manager works with the `with ... as ...` syntax.

We could try to use `contextlib.contextmanager` here but it'll complicate things a bit, so let's not.

Instead of relying on `time.time`, we could use `timeit.default_timer` which has always used the highest available resolution clock on the current operating system we're running on. Or better yet, we could just use `time.perf_counter`, which has done the same thing since Python 3.3 (`timeit.default_timer` turned into an alias for `time.perf_counter` in Python 3.3).

    from time import perf_counter

    class Timer:

        """Context manager to time a code block."""

        def __enter__(self):
            self.start = perf_counter()
            return self

        def __exit__(self, *args):
            self.end = perf_counter()
            self.elapsed = self.end - self.start

# Bonus #1

For the first bonus you needed to record the times from each usage of our context manager objects into a `runs` list.

We could do that by making an new list in a `runs` attribute in our initializer and then appending to that list in our `__exit__` method.

    from timeit import default_timer

    class Timer:

        """Context manager to time a code block."""

        def __init__(self):
            self.runs = []

        def __enter__(self):
            self.start = default_timer()
            return self

        def __exit__(self, *args):
            self.end = default_timer()
            self.elapsed = self.end - self.start
            self.runs.append(self.elapsed)

# Bonus #2

For the second bonus we needed to make our context manager also work as a decorator.

You might have tried to use `contextlib.ContextDecorator` for this. Unfortunately the `ContextDecorator` doesn't work quite the way we need it to.

We need our `@timer`-decorated function to have a `runs` attribute and an `elapsed` attribute. One way to do this would be to replace the decorated function with an instance of our `Timer` class and then make our `Timer` instances callable. We can do that by making a `__call__` method:

        def __init__(self, func=None):
            self.func = func
            self.runs = []

        def __call__(self, *args, **kwargs):
            with self:
                return self.func(*args, **kwargs)

Our initializer now optionally accepts a function to decorate. If our `Timer` instance is called (remember that our `Timer` instance is replacing the decorated function) then our `__call__` method will be called. That will call the decorated function, wrapped in our own context manager instance (with that `with self`).

Note that we could have implemented `__call__` like this:

        def __call__(self, *args, **kwargs):
            self.__enter__()
            try:
                return self.func(*args, **kwargs)
            finally:
                self.__exit__()

But we're really just re-implementing Python's `with` block here by ensuring the `__enter__` method is called before `self.func` is called and then ensuring the `__exit__` method is always called, even if an exception occurs.

It's better to just use a `with` block.

One downside to using a class as a decorator is that our decorated class will lose its name, function signature, and docstring:

    >>> @Timer
    ... def do_something(x):
    ...     """Return x squared."""
    ...     return x ** 2
    ...
    >>> do_something
    <__main__.Timer object at 0x7f6eb33455c0>
    >>> do_something.__doc__
    'Context manager to time a code block.'

The `functools.wraps` helper exists in the standard library to help us with this issue, but _it only works on functions_!

If we wanted to, we could make `Timer` a function that either returns a class instance or returns a decorated function which will also store the appropriate attributes on itself (as if it were a class instance):

    from functools import wraps
    from timeit import perf_counter

    class TimerContextManager:

        """Context manager to time a code block."""

        def __init__(self, func=None):
            self.func = func
            self.runs = []

        def __enter__(self):
            self.start = perf_counter
            return self

        def __exit__(self, *args):
            self.end = perf_counter
            self.elapsed = self.end - self.start
            self.runs.append(self.elapsed)

    def Timer(func=None):
        if func is None:
            return TimerContextManager()
        else:
            timer = TimerContextManager()
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    with timer:
                        return func(*args, **kwargs)
                finally:
                    wrapper.elapsed = timer.elapsed
                    wrapper.runs = timer.runs
            return wrapper

But I think this is more hassle than it's worth. If we decided we really want our decorator to be well-behaved by being invisible, we could use the

    from time import perf_counter
    from wrapt import ObjectProxy

    class Timer(ObjectProxy):

        """Context manager to time a code block."""

        def __init__(self, func=None):
            super().__init__(func or (lambda: None))
            self.runs = []

        def __call__(self, *args, **kwargs):
            with self:
                return self.__wrapped__(*args, **kwargs)

        def __enter__(self):
            self.start = perf_counter()
            return self

        def __exit__(self, *args):
            self.end = perf_counter()
            self.elapsed = self.end - self.start
            self.runs.append(self.elapsed)

If we use the `wrapt` library's `ObjectProxy` class in this way, our decorator will be well-behaved:

    >>> @Timer
    ... def do_something(x):
    ...     """Return x squared."""
    ...     return x ** 2
    ...
    >>> help(do_something)
    Help on function do_something in module __main__:

    do_something(x)
        Return x squared.

You'll notice I had a weird `func or (lambda: None)` hack to make this `ObjectProxy` work as a context manager or as a decorator.

I don't think this effort is worthwhile in most cases. I recommend just ignoring the problem and having a slightly-poorly-behaved decorator.

# Bonus #3

For the third bonus you needed to add a number of statistics attributes to your `Timer`: `min`, `max`, `mean`, and `median`.

We could implement `mean` and `median` ourselves, but the Python standard library already has fast implementations of these operations in the `statistics` module:

    from statistics import mean, median

So we could modify our `__exit__` method like this:

        def __exit__(self, *args):
            self.end = perf_counter()
            self.elapsed = self.end - self.start
            self.runs.append(self.elapsed)
            self.mean = mean(self.runs)
            self.median = median(self.runs)
            self.min = min(self.runs)
            self.max = max(self.runs)

This would compute each of these stats once every time our context manager is exited.

If these aren't checked often, we could delay computing them until these attributes are accessed by using properties instead:

        @property
        def mean(self):
            return mean(self.runs)

        @property
        def median(self):
            return median(self.runs)

        @property
        def min(self):
            return min(self.runs)

        @property
        def max(self):
            return max(self.runs)

Readability-wise I think I like this approach slightly better, but I'm fine with either one.

Here's a fully working solution that passes all three bonuses:

    from statistics import mean, median
    from time import perf_counter

    class Timer:

        """Context manager to time a code block."""

        def __init__(self, func=None):
            self.func = func
            self.runs = []

        def __call__(self, *args, **kwargs):
            with self:
                return self.func(*args, **kwargs)

        def __enter__(self):
            self.start = perf_counter()
            return self

        def __exit__(self, *args):
            self.end = perf_counter()
            self.elapsed = self.end - self.start
            self.runs.append(self.elapsed)
            self.mean = mean(self.runs)
            self.median = median(self.runs)
            self.min = min(self.runs)
            self.max = max(self.runs)

I hope you learned something this week about context managers, decorators, timing, or the statistics module!