# Solution: suppress

Hiya,

If you haven't attempted to solve suppress yet, close this email and go do that now before reading on. If you have attempted solving suppress, read on...

This week you needed to create a context manager that suppresses specific exceptions.

To make a context manager, we need to create an object that has `__enter__` and a `__exit__` methods.

Here's one way to do that:

    class suppress:

        """Context manager that suppresses exceptions of given type."""

        def __init__(self, exception_type):
            self.exception_type = exception_type

        def __enter__(self):
            pass

        def __exit__(self, exception_type, exception, traceback):
            if isinstance(exception, self.exception_type):
                return True
            else:
                return False

We can use this context manager like this:

    >>> with suppress(ValueError):
    ...     x = int('hello')
    ...

Calling suppress will invoke our initializer (`__init__`). When we enter our `with` block, our `__enter__` method will be called. When we exit our `with` block, our `__exit__` method will be called.

Our `__exit__` method is where the real work happens. This method will be passed [three arguments](https://docs.quantifiedcode.com/python-anti-patterns/correctness/exit_must_accept_three_arguments.html), which will be None if no exception is raised and will contain information about the exception otherwise. We're checking whether our exception is an instance of the given exception type and returning True if it is and False otherwise.

Note that our `__enter__` method is empty. We have to implement this method, but our context manager doesn't have any setup work to do so we've made an empty method.

You may have tried to implement `__exit__` using the "type" function:

        def __exit__(self, exception_type, exception, traceback):
            if type(exception) == self.exception_type:
                return True
            else:
                return False

But this direct type check is too exact for our purposes because it doesn't handle inheritance. `KeyError` inherits from `LookupError` and if a `KeyError` is raised but we're suppressing `LookupError` exceptions, we want to make sure that also includes `KeyError` exceptions. So we need to use `isinstance`.

        def __exit__(self, exception_type, exception, traceback):
            if isinstance(exception, self.exception_type):
                return True
            else:
                return False

If `__exit__` returns something "truthy", the exception raised in our context block will be suppressed, but if something "falsey" is returned then the exception will keep bubbling up the call stack of our program.

By default functions return `None`, which is "falsey", so we can leave off the `else` clause, though it might make our code less readable.

Much better than this though, we could leave off the `if` statement entirely:

        def __exit__(self, exception_type, exception, traceback):
            return isinstance(exception, self.exception_type)

The `isinstance` function returns either `True` or `False`, which is exactly what we're looking for.

Instead of using `isinstance`, we could have used `issubclass`:

        def __exit__(self, exception_type, exception, traceback):
            return exception and issubclass(exception_type, self.exception_type)

This requires an extra check though (that `exception and ...`) because if no exception was raised, the exception type will be `None`. `None` isn't a class and `issubclass` raises an exception when given non-classes.

So far my favorite solution to this problem is the single-line `isinstance` call.

But my preferred solution is this one:

    from contextlib import contextmanager

    @contextmanager
    def suppress(exception_type):
        """Context manager that suppresses exceptions of given type."""
        try:
            yield
        except exception_type:
            pass

Here we're using a helper utility called `contextmanager` which will take a generator function with a single `yield` statement and return a context manager class with working `__enter__` and `__exit__` methods.

I like this solution because it's clear that we're handling an exception here. We're able to write our code as if we're wrapping everything in our `with` block wherever our `yield` call is.

If you've never seen that `@` syntax before, that's a decorator. We'll be making our own decorator in bonus 3.

Exception-handling is one of my favorite uses for the `contextmanager` decorator.

There's one solution I need to discuss before we move to the first bonus:

    from contextlib import suppress

This is the simplest solution. We're not implementing something here because the standard library already has a suppress context manager in it!

# Bonus #1

For the first bonus, you were supposed to allow your context manager to accept any number of exceptions to suppress.

The `contextlib.suppress` context manager actually does this already. If we're going to do this ourselves, this could be as simple as accepting any number of arguments to our `contextmanager`-decorated generator function:

    from contextlib import contextmanager

    @contextmanager
    def suppress(*exception_types):
        """Context manager that suppresses exceptions of given types."""
        try:
            yield
        except exception_types:
            pass

This works because `*exception_types` captures all the given arguments into a tuple and the except clause happily accepts a tuple of exception types (that's what that comma-separated `except ValueError, TypeError:` syntax you normally see is actually doing.

Likewise we can do this:

    class suppress:

        """Context manager that suppresses exceptions of given type."""

        def __init__(self, *exception_types):
            self.exception_types = exception_types

        def __enter__(self):
            pass

        def __exit__(self, exception_type, exception, traceback):
            return isinstance(exception, self.exception_types)

This works because `isinstance` will accept a single class or a tuple of classes to check. The `issubclass` function works the same way.

# Bonus #2

For the second bonus, you had to allow your suppress context manager to be used with the `with ... as ...` syntax, like this:

    with suppress(ValueError) as context:
        int('hello')
    print("Exception info:", context.exception)
    print("Traceback info:", context.traceback)

We want any exception raised to be stored on the object

To do this we need our context manager's `__enter__` method to return an object.

Here's one way to do that:

    from contextlib import contextmanager
    import sys

    class ExceptionInfo:
        exception = None
        traceback = None

    @contextmanager
    def suppress(*exception_types):
        """Context manager that suppresses exceptions of given types."""
        info = ExceptionInfo()
        try:
            yield info
        except exception_types as e:
            info.exception = e
            info.traceback = sys.exc_info()[2]

Here we're creating a new class to store our exception information. We create an instance of this class and yield it to our with block, which passes it to the variable after the `as` in our `with` block.

We're using `sys.exc_info` here to get the traceback information for the current exception.

In Python 3, there's another way to get the traceback information for the current exception:

    @contextmanager
    def suppress(*exception_types):
        """Context manager that suppresses exceptions of given types."""
        info = ExceptionInfo()
        try:
            yield info
        except exception_types as e:
            info.exception = e
            info.traceback = e.__traceback__

Every raised exception in Python 3 has a `__traceback__` attribute that stores the traceback object associated with that exception.

If you're in Python 3.7, you could make that `ExceptionInfo` class we made a little friendlier by using the `dataclass` decorator:

    from dataclasses import dataclass
    from types import TracebackType
    from typing import Optional

    @dataclass
    class ExceptionInfo:
        exception: Optional[Exception] = None
        traceback: Optional[TracebackType] = None

This dictates the types excepted for our attributes, which acts as documentation-in-code in a sense.

This requires more lines of code and it makes our code a bit uglier, but this gives our class a helpful string representation for those using it.

Alternatively we could go the other direction and use [types.SimpleNamespace](https://docs.python.org/3/library/types.html#types.SimpleNamespace) instead of defining a new class at all:

    from contextlib import contextmanager
    from types import SimpleNamespace

    @contextmanager
    def suppress(*exception_types):
        """Context manager that suppresses exceptions of given types."""
        info = SimpleNamespace()
        try:
            yield info
        except exception_types as e:
            info.exception = e
            info.traceback = e.__traceback__

I've shown you solutions to this second bonus problem using the `contextmanager` decorator only. But this bonus might actually be a bit clearer if we use a class-based context manager instead:

    class suppress:

        """Context manager that suppresses exceptions of given types."""

        def __init__(self, *exception_types):
            self.exception_types = exception_types

        def __enter__(self):
            return self

        def __exit__(self, exception_type, exception, traceback):
            self.exception = exception
            self.traceback = traceback
            return isinstance(exception, self.exception_types)

Here our `__enter__` method returns `self`, which passes our `suppress` object to the variable after `as` in our with block (`with suppress(ValueError) as context` will assign context to that suppress instance now).

This way we don't need an extra object to store our exception and traceback information on. We could simple store that information on our own object.

While I prefer the clarity of the try-except in our `contextmanager`-decorated generator function, I think the cleanness of using our suppress object to store context information makes the class-based approach superior in this case.

# Bonus #3

For the third bonus, you needed to make your context manager work as a decorator as well as a context manager.

This means that we can do this:

    @suppress(TypeError):
    def len_or_none(thing):
        return len(thing)

Which is exactly the same as doing this:

    def len_or_none(thing):
        return len(thing)

    len_or_none = suppress(TypeError)(len_or_none)

That's how that `@`-syntax for decorators works in Python.

So we need to make our suppress objects callable, so they accept a function and return a function that wraps the original function in our context manager.

    from functools import wraps

    class suppress:

        """Context manager that suppresses exceptions of given types."""

        def __init__(self, *exception_types, default=None):
            self.exception_types = exception_types
            self.default = None

        def __call__(self, function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                with self:
                    return function(*args, **kwargs)
            return wrapper

        def __enter__(self):
            return self

        def __exit__(self, exception_type, exception, traceback):
            self.exception = exception
            self.traceback = traceback
            return isinstance(exception, self.exception_types)

We're implementing a `__call__` method on our suppress objects so they'll be callable. They'll be called as a decorator, so they'll accept our original function and they're supposed to return a new wrapper function around our original function.

Our `wrapper` function uses our `suppress` object (that `with self` is using our object as a context manager) to wrap the call to our original function with the arguments that have been provided to us.

That `functools.wraps` thing is a helper for creating wrapper-functions that borrow the features of their original function. The documentation for [wraps](https://docs.python.org/3/library/functools.html#functools.wraps) isn't very helpful. [This link on wraps](https://stackoverflow.com/a/309000/98187) explains it a little bit further.

I've explained using classes as decorators [in a past Python chat](https://www.crowdcast.io/e/decorators-2/1/q/-L8x2wcxH6A5UoScEF5t) and Bruce Eckel [wrote about this pattern here](https://python-3-patterns-idioms-test.readthedocs.io/en/latest/PythonDecorators.html#function-decorators). This works because both classes and functions are [callables](https://treyhunner.com/2019/04/is-it-a-class-or-a-function-its-a-callable/) and in Python we usually care more about whether something is a _callable_ than whether it is a function, a class, or an instance of a class.

You can look into the specifics of decorators and `wraps` on your own if you're curious. I'd like to move to another another way of solving this particular problem.

Instead of making our own decorator class, we can use the `ContextDecorator` class, which implements a `__call__` method for us:

    from contextlib import ContextDecorator

    class suppress(ContextDecorator):

        """Context manager that suppresses exceptions of given types."""

        def __init__(self, *exception_types, default=None):
            self.exception_types = exception_types
            self.default = None

        def __enter__(self):
            return self

        def __exit__(self, exception_type, exception, traceback):
            self.exception = exception
            self.traceback = traceback
            return isinstance(exception, self.exception_types)

You will eventually want to understand decorators a bit, so you might want to add them to your learning to-do list to check out briefly in the next couple months if you haven't already.

Somewhat surprisingly, we can also use our contextmanager-decorated generator function as a decorator without any modifications:

    from contextlib import contextmanager

    class ExceptionInfo:
        exception = None
        traceback = None

    @contextmanager
    def suppress(*exception_types):
        """Context manager that suppresses exceptions of given types."""
        info = ExceptionInfo()
        try:
            yield info
        except exception_types as e:  # type: ignore
            info.exception = e
            info.traceback = e.__traceback__

This works because the `contextmanager` decorator function is implemented using `ContextDecorator`, so we can always use context managers that we create this way as decorators.

By the way, the `contextlib.suppress` context manager can also be used as a decorator. If you ever need a suppress context manager, I'd recommend reaching for that one instead of rolling your own.

If you were inspired by the type annotations in our `dataclasses` version of `ExceptionInfo` in bonus 2, you could decide to adopt [mypy](http://mypy-lang.org/) in your code and go all in on type annotations.

This can make for some pretty nasty code sometimes though:

    from contextlib import contextmanager
    from dataclasses import dataclass
    from types import TracebackType
    from typing import Iterator, Optional

    @dataclass
    class ExceptionInfo:
        exception: Optional[Exception] = None
        traceback: Optional[TracebackType] = None

    @contextmanager
    def suppress(*exception_types: Exception) -> Iterator[ExceptionInfo]:
        """Context manager that suppresses exceptions of given types."""
        info = ExceptionInfo()
        try:
            yield info
        except exception_types as e:  # type: ignore
            info.exception = e
            info.traceback = e.__traceback__

That `except` line in particular is unfortunate. Running `mypy --strict` against this code without that `# type: ignore` comment will incorrectly complain about the `exception_types` variable.

I hope you learned something new this week!