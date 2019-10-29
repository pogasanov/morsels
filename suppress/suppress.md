# suppress
##### Assigned from Advanced Level on 10/28/2019

Hey!

This week I'd like you to create a context manager. Context managers use a `with` block to bookend a block of code with automatic setup and teardown steps.

Your context manager, `suppress`, should suppress exceptions of a given type:

    >>> with suppress(NameError):
    ...     print("Hi!")
    ...     print("It's nice to meet you,", name)
    ...     print("Goodbye!")
    ...
    Hi!
    >>> with suppress(TypeError):
    ...     print("Hi!")
    ...     print("It's nice to meet you,", name)
    ...     print("Goodbye!")
    ...
    Hi!
    Traceback (most recent call last):
      File "<stdin>", line 3, in <module>
    NameError: name 'name' is not defined
    >>> x = 0
    >>> with suppress(ValueError):
    ...     x = int('hello')
    ...
    >>> x
    0

What I mean by "suppress" is that if the given exception type is raised, that exception should be caught and _muted_ in a sense.

To solve this exercise, you'll want to lookup how to create a context manager in Python.

For the first bonus, I'd like you to make your `suppress` context manager accept any number of exceptions to suppress ✔️:

    >>> with suppress(ValueError, TypeError):
    ...     x = int('hello')
    ...
    >>> with suppress(ValueError, TypeError):
    ...     x = int(None)
    ...

For the second bonus, I'd like you to allow your context manager to store the exception and traceback information on an object that can be accessed using the `with X as Y` syntax ✔️:

    >>> with suppress(ValueError, TypeError) as context:
    ...     x = int('hello')
    ...
    >>> context.exception
    ValueError("invalid literal for int() with base 10: 'hello'",)
    >>> context.traceback
    <traceback object at 0x7fe829bc3bc8>

The `exception` and `traceback` attributes should be `None` when no exception was suppressed.

If you manage to solve the main problem and both of the first two bonuses with time remaining, I have a third bonus for you.

For the third bonus I'd like you to allow your context manager to be used as a decorator as well ✔️:

    >>> @suppress(TypeError)
    ... def len_or_none(thing):
    ...     return len(thing)
    ...

This decorator should essentially wrap your function in a call to the suppress context manager:

    >>> len_or_none('hello')
    5
    >>> len_or_none(64)
    >>> len_or_none([2, 4, 8])
    3
    >>> len_or_none()
    >>> len_or_none([])
    0

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/ded322173d47424581be45adaeeca90d/tests/). You'll need to write your function in a module named suppress.py next to the test file. To run the tests you'll run "python test_suppress.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.