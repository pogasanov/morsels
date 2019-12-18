# Solution: record_calls

Hey!

If you haven't attempted to solve record_calls yet, close this email and go do that now before reading on. If you have attempted solving record_calls, read on...

This week you needed to make a decorator function, record_calls, that will record the number of times the decorated function is called.

Here's one attempt at this:

    def record_calls(func):
        """Record calls to the given function."""
        def wrapper(*args):
            wrapper.call_count += 1
            return func(*args)
        wrapper.call_count = 0
        return wrapper

Decorator functions accept a function and return a function, which we're doing here. The function we're returning wraps around our original function and calls it with the arguments given to it.

We're storing a call_count attribute on our wrapper function. We have to set that call_count attribute to 0 after creating our wrapper function so that we can then increment it inside our wrapper function.

This might seem a little odd but it works. Functions are allowed to have attributes and you can add or update their attributes at runtime.

This function doesn't quite work though. The wrapper function that our decorator returns doesn't accept keyword arguments, so my_function(1, 2) would work, but my_function(x=1, y=2) wouldn't.

We can fix that by accepting and passing along keyword arguments given to us:

    def record_calls(func):
        """Record calls to the given function."""
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            return func(*args, **kwargs)
        wrapper.call_count = 0
        return wrapper

This decorator function works fine. There's another way to solve this problem though.

Functions in Python are allowed to accept functions, return other functions, and even create functions inside themselves... all of which we're doing here.

But a decorator function isn't necessarily a function that accepts a function and returns a function. You can think of a decorator as a callable that accepts a callable and returns a callable.

Classes are callable. They give you instances when you call them. And class instances can also be callable, if they implement a `__call__` method. So we can create a decorator like this too:

    class record_calls:

        """Record calls to the given function."""

        def __init__(self, func):
            self.call_count = 0
            self.func = func

        def __call__(self, *args, **kwargs):
            self.call_count += 1
            return self.func(*args, **kwargs)

This might seem a little odd, but this has some benefits. With this decorator, we're trying to record state via a call_count on our wrapper function. When we use a callable object, we can just record that state on the object itself.

It's less typical to see a decorator implemented using a class, but it can improve readability at times. Personally, I find this implementation a little more clear for this particular decorator.

# Bonus #1

For the first bonus we were supposed to make our wrapper function steal the name, documentation, and type signature of our original function.

We could try to do this manually:

    def record_calls(func):
        """Record calls to the given function."""
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            return func(*args, **kwargs)
        wrapper.call_count = 0
        wrapper.__name__ = func.__name__
        wrapper.__qualname__ = func.__qualname__
        wrapper.__doc__ = func.__doc__
        wrapper.__annotations__ = func.__annotations__
        return wrapper

But that doesn't quite pass our tests because we're missing the type signature here. Also this is kind of a pain.

A better way to do this is to use functools.wraps, which is a helper function specifically designed for making it easier to create decorator functions:

    from functools import wraps

    def record_calls(func):
        """Record calls to the given function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            return func(*args, **kwargs)
        wrapper.call_count = 0
        return wrapper

The wraps utility is a function which accepts a function and returns a decorator for use on our decorator wrapper function. You don't need to read that sentence again. It's confusing and mostly unimportant. The important thing to remember is that functools.wraps exists and you can look up how to use it whenever you need to make a decorator function.

If we wanted to use our class-based approach from before, we'll need to use functools.update_wrapper to steal the information from our function and update our record_calls class instance:

    from functools import update_wrapper

    class record_calls:

        """Record calls to the given function."""

        def __init__(self, func):
            self.call_count = 0
            self.func = func
            update_wrapper(self, func)

        def __call__(self, *args, **kwargs):
            self.call_count += 1
            return self.func(*args, **kwargs)

This doesn't quite pass our tests though. Unfortunately, the record_calls class will still have an unhelpful string representation and it still won't have quite the right documentation.

We could try to fix this ourselves, but it's kind of a pain. The easiest way to fix this is to rely on the third-party wrapt library.

    import wrapt

    class record_calls(wrapt.ObjectProxy):

        """Record calls to the given function."""

        def __init__(self, func):
            super().__init__(func)
            self.call_count = 0

        def __call__(self, *args, **kwargs):
            self.call_count += 1
            return self.__wrapped__(*args, **kwargs)

The wrapt library has a lot of decorator helpers in it, but the one that we're concerned with is the one that allows us to make a class which will act as a seamless wrapper around a function. It's a little bit awkward to use wrapt.ObjectProxy, but it works.

I don't usually show third-party libraries in these solutions and I didn't expect you to discover this one, but I wanted you to know it exists because it can come in handy at times (for making any kind of decorator, not just ones that use classes).

I prefer the non-class approach here because I think the added complexity of wrapt doesn't help quite enough to justify its use.

# Bonus #2

For the second bonus, we needed to add a list of call objects onto our record_calls function, each of which will contain positional and keyword arguments for each call made to our function.

    from functools import wraps

    class Call:
        def __init__(self, args, kwargs):
            self.args = args
            self.kwargs = kwargs

    def record_calls(func):
        """Record calls to the given function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            wrapper.calls.append(Call(args, kwargs))
            return func(*args, **kwargs)
        wrapper.call_count = 0
        wrapper.calls = []
        return wrapper

Here we're initializing an empty calls list on our function and then appending a Call object each time our function is called. Our Call objects are just a constructor that accepts two arguments (args and kwargs) and stores them on itself.

Another way to create that Call object is using a namedtuple:

    from collections import namedtuple
    from functools import wraps

    Call = namedtuple('Call', 'args kwargs')

    def record_calls(func):
        """Record calls to the given function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            wrapper.calls.append(Call(args, kwargs))
            return func(*args, **kwargs)
        wrapper.call_count = 0
        wrapper.calls = []
        return wrapper

This object is a bit different because it's immutable and essentially acts like a tuple, except it also has "args" and "kwargs" attributes on it.

Since Python 3.5, there's a slightly nicer way to make a namedtuple:

    from typing import NamedTuple
    from functools import wraps

    class Call(NamedTuple):
        args: tuple
        kwargs: dict

    def record_calls(func):
        """Record calls to the given function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            wrapper.calls.append(Call(args, kwargs))
            return func(*args, **kwargs)
        wrapper.call_count = 0
        wrapper.calls = []
        return wrapper

Here we're explicitly noting that args is a tuple and kwargs is a dictionary, which makes for great documentation.

If you're on Python 3.7 or greater, I'd recommend a different way to define this Call object:

    from dataclasses import dataclass
    from functools import wraps

    @dataclass
    class Call:
        args: tuple
        kwargs: dict

    def record_calls(func):
        """Record calls to the given function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            wrapper.calls.append(Call(args, kwargs))
            return func(*args, **kwargs)
        wrapper.call_count = 0
        wrapper.calls = []
        return wrapper

Here we're creating a dataclass called Call which accepts args and kwargs arguments and defines attributes of the same name on itself. Unlike a namedtuple, this object is mutable (it can be changed) and it is not tuple- like. Like a namedtuple, it has a nice string representation and equality operators are implemented in a sensible way by default.

If you're on a version of Python before 3.7, you can install dataclasses from the Python Package Index to start using this feature without upgrading.

This is the solution I'd recommend for this bonus problem.

# Bonus #3

The third bonus is tricky. We were required with this bonus to include a unique NO_RETURN value in our module that would be returned if our function didn't return (because it raised an exception).

We needed this value to be unique, so it's best to create a sentinel object that would be neither identical to anything else nor equal to pretty much anything else:

    NO_RETURN = object()

After that, we needed to actually assign to the return_value and exception attributes on our Call objects appropriately:

    def record_calls(func):
        """Record calls to the given function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            call = Call(args, kwargs)
            wrapper.calls.append(call)
            try:
                call.exception = None
                call.return_value = func(*args, **kwargs)
            except BaseException as e:
                call.exception = e
                call.return_value = NO_RETURN
                raise
            return call.return_value
        wrapper.call_count = 0
        wrapper.calls = []
        return wrapper

We try to set exception to None and return_value to the return_value of our function. If an exception is raised while we call our function, we set the exception value to the exception instance and then we set return_value to NO_RETURN and continue raising the exception.

Note that we're creating those exception and return_value attributes on our objects manually. But we could make our Call objects aware of those and set a default value for them:

    from dataclasses import dataclass
    from functools import wraps
    from typing import Any, Optional

    NO_RETURN = object()

    @dataclass
    class Call:
        args: tuple
        kwargs: dict
        return_value: Any = NO_RETURN
        exception: Optional[BaseException] = None

    def record_calls(func):
        """Record calls to the given function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.call_count += 1
            call = Call(args, kwargs)
            wrapper.calls.append(call)
            try:
                call.return_value = func(*args, **kwargs)
            except BaseException as e:
                call.exception = e
                raise
            return call.return_value
        wrapper.call_count = 0
        wrapper.calls = []
        return wrapper

Our Call object now defaults return_value to NO_RETURN and exception to None. We then assign those values manually as appropriate.

I hope you got some good practice with decorators this week!