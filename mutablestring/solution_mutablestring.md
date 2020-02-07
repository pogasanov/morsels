# Solution: MutableString

Heya!

If you haven't attempted to solve MutableString yet, close this email and go do that now before reading on. If you have attempted solving MutableString, read on...

This week you needed to make a class called `MutableString`, which will act like a "mutable" string.

At first you needed to focus on index assignment, string concatenation, and length.

Here's one way to do this:

    class MutableString:
        def __init__(self, data=""):
            self.data = str(data)
        def __eq__(self, other):
            return self.data == other
        def __str__(self):
            return self.data
        def __repr__(self):
            return repr(self.data)
        def __len__(self):
            return len(self.data)
        def __add__(self, other):
            if isinstance(other, MutableString):
                return self.data + other.data
            else:
                return self.data + other
        def __getitem__(self, index):
            return self.data[index]
        def __contains__(self, substring):
            return substring in self.data
        def __setitem__(self, index, value):
            chars = list(self.data)
            chars[index] = value
            self.data = "".join(chars)
        def replace(self, *args, **kwargs):
            return self.data.replace(*args, **kwargs)
        def upper(self):
            return self.data.upper()
        def lower(self):
            return self.data.lower()
        def endswith(self, *args, **kwargs):
            return self.data.endswith(*args, **kwargs)

This class has two string representations (`__repr__` and `__str__`), supports equality and inequality (`__eq__`), and supports concatenation and length (`__add__`, `__len__`). Note that we don't need both `__eq__` and `__ne__` because in Python 3, `__ne__` just calls `__eq__`.

All that is just to make our `MutableString` object act kind of like a string.

The `__setitem__` is to make our string "mutable".

In our `__setitem__` we're making a list out of the characters in our `self.data` string, updating the given item in this list, and then joining these character strings back together and storing them back in `self.data`.

We can't mutate strings so we have to build up a new modified `self.data` string somehow.

Here's another way we could have done `__setitem__`:

        def __setitem__(self, index, value):
            self.data = self.data[:index] + value + self.data[index+1:]

We're avoiding converting our string to a list and back here. Instead we're taking two substrings and concatenating them with `value` in the middle.

If we wanted to avoid all the repetition of proxying every method call to `self.data`, we could make a helper function to create each of these methods:

    from functools import wraps

    class MutableString:
        def __init__(self, data=""):
            self.data = str(data)
        def __eq__(self, other):
            return self.data == other
        def __add__(self, other):
            if isinstance(other, MutableString):
                return self.data + other.data
            else:
                return self.data + other
        def __setitem__(self, index, value):
            chars = list(self.data)
            chars[index] = value
            self.data = "".join(chars)
        def _proxy(methodname):
            @wraps(methodname)
            def wrapper(self, *args, **kwargs):
                return getattr(self.data, methodname)(*args, **kwargs)
            return wrapper
        __str__ = _proxy('__str__')
        __repr__ = _proxy('__repr__')
        __len__ = _proxy('__len__')
        __getitem__ = _proxy('__getitem__')
        __contains__ = _proxy('__contains__')
        replace = _proxy('replace')
        lower = _proxy('lower')
        upper = _proxy('upper')
        endswith = _proxy('endswith')

This `_proxy` function takes a method name and returns a new function which loops that method up on `self.data`, calls it with the incoming arguments, and then returns.

We're using the `functools.wraps` decorator to preserve the name of the method (`MutableString.replace` should be a function named `replace`, not `wrapper`).

We can't proxy `__eq__` to the string beneath us because `==` does more than just call `__eq__`: if `NotImplemented` is returned (which it will be when another `MutableString` object is given) then we delegate to the other object's `__eq__` instead.

Here's a much simpler way to solve this problem:

    from collections import UserString

    class MutableString(UserString):
        def __setitem__(self, index, value):
            chars = list(self.data)
            chars[index] = value
            self.data = "".join(chars)

Here we've decided not to do comparisons, concatenation, and various string methods on our own but instead delegate to [collections.UserString](https://docs.python.org/3/library/collections.html#collections.UserString).

If you need to make your own string-like type, `collections.UserString` can be handy for this.

You might have thought to inherit from `str` and found it didn't work. Inheriting from `collections.UserString` works because we're _wrapping_ around a string whereas `str` _is_ a string (and immutability is an inherent property of strings).

# Bonus #1

For our first bonus we needed to allow assigning to slices and deleting slices.

Our current solutions actually allows for assigning slices already.

To add deleting slices we'll need a `__delitem__` method:

        def __delitem__(self, index):
            chars = list(self.data)
            del chars[index]
            self.data = "".join(chars)

This passes because lists support slice assignment and they support slice deletions. So we didn't have to do anything special to handle `slice` objects because lists already do that work for us.

Here's that method in our (still short) `UserString` solution:

    from collections import UserString

    class MutableString(UserString):
        def __setitem__(self, index, value):
            chars = list(self.data)
            chars[index] = value
            self.data = "".join(chars)
        def __delitem__(self, index):
            chars = list(self.data)
            del chars[index]
            self.data = "".join(chars)

# Bonus #2

For the second bonus you needed to make sure your `MutableString` objects returned `MutableString` objects when indexed, sliced, iterated over, and more.

The `UserString`-inheriting version of `MutableString` already passes this bonus: `MutableString` objects are always returned from it.

To get our manually-implemented `MutableString` class working, we'll need to wrap lots of return values in `MutableString` calls.

If we're using that `_proxy` helper we saw in the base problem, we could add a `MutableString` call to it:

        def _proxy(methodname):
            @wraps(methodname)
            def wrapper(self, *args, **kwargs):
                ret = getattr(self.data, methodname)(*args, **kwargs)
                return MutableString(ret) if isinstance(ret, str) else ret

This wraps the `str` return values in a `MutableString` call (we check for `str` return values so `lower`, `endswith`, and `__contains__` don't have their booleans/integers become `MutableString` objects).

This doesn't quite work though: the `__str__` and `__repr__` methods must return strings, not `MutableString` objects.

We can add an extra `wrap` argument to fix this:

        def _proxy(methodname, wrap=True):
            @wraps(methodname)
            def wrapper(self, *args, **kwargs):
                ret = getattr(self.data, methodname)(*args, **kwargs)
                return MutableString(ret) if isinstance(ret, str) and wrap else ret
            return wrapper
        __str__ = _proxy('__str__', wrap=False)
        __repr__ = _proxy('__repr__', wrap=False)
        __len__ = _proxy('__len__')
        __getitem__ = _proxy('__getitem__')
        __contains__ = _proxy('__contains__')
        replace = _proxy('replace')
        lower = _proxy('lower')
        upper = _proxy('upper')
        endswith = _proxy('endswith')

Additionally, we'll also need to make sure our `__add__` method wraps its return value in `MutableString` calls:

        def __add__(self, other):
            if isinstance(other, MutableString):
                return MutableString(self.data + other.data)
            else:
                return MutableString(self.data + other)

If we did this without that `_proxy` method, we'd need to make sure many of our string-returning methods return `MutableString` objects instead:

        def replace(self, *args, **kwargs):
            return MutableString(self.data.replace(*args, **kwargs))
        def upper(self):
            return MutableString(self.data.upper())
        def lower(self):
            return MutableString(self.data.lower())
        def endswith(self, *args, **kwargs):
            return self.data.endswith(*args, **kwargs)

# Bonus #3

For the third bonus you needed to make `append`, `insert`, and `pop` methods.

We could implement them pretty much the same way as our other methods:

        def append(self, item):
            chars = list(self.data)
            chars.append(item)
            self.data = "".join(chars)

        def insert(self, index, item):
            chars = list(self.data)
            chars.insert(index, item)
            self.data = "".join(chars)

        def pop(self, index=-1):
            chars = list(self.data)
            ret = chars.pop(index)
            self.data = "".join(chars)
            return MutableString(ret)

We can actually avoid implementing `append` and `pop` if we instead inherit from `collections.abc.MutableSequence`.

Here's the `UserString`-inheriting version of our `MutableString` class which implements `insert`, `__setitem__`, and `__delitem__`, and gets `append` and `pop` for free:

    from collections.abc import MutableSequence
    from collections import UserString

    class MutableString(MutableSequence, UserString):
        def __setitem__(self, index, value):
            chars = list(self.data)
            chars[index] = value
            self.data = "".join(chars)
        def __delitem__(self, index):
            chars = list(self.data)
            del chars[index]
            self.data = "".join(chars)
        def insert(self, index, item):
            chars = list(self.data)
            chars.insert(index, item)
            self.data = "".join(chars)

We're inheriting from both `MutableSequence` and `UserString` here. The `MutableSequence` abstract base class will implement `append`, `pop`, and more if we have `__setitem__`, `__delitem__`, and `insert` implemented.

If you're trying to create something that looks and acts like a mutable sequence, the [collections.abc.MutableSequence](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes) base class is a helper function that'll make that work easier.

We're practicing multiple inheritance here, which often isn't recommended. In this case it's likely fine though: the `MutableSequence` methods delegate to the methods we've already implemented and any methods that aren't defined there will fall back to the `UserString` versions.

You might notice that there's a lot of repetition in `__setitem__`, `__delitem__`, and `insert`. Those three methods look almost identical: of the three lines in those methods the only one that's different is the middle one. It would be neat if we could use a context manager to sandwich those not-quite-the-same middle lines.

Like this:

        def __setitem__(self, index, value):
            with self.chars() as chars:
                chars[index] = value
        def __delitem__(self, index):
            with self.chars() as chars:
                del chars[index]
        def insert(self, index, value):
            with self.chars() as chars:
                chars.insert(index, value)

For this to work we'd need to implement a `chars` method which returns a context manager that returns a new list on entrance and then assigns `self.data` to the correct string (based on that list) on exit.

Here's one way to do that:

        def chars(self):
            string = self
            class StringWrapper:
                def __enter__(self):
                    self.chars = list(string.data)
                    return self.chars
                def __exit__(self, *args):
                    string.data = "".join(self.chars)
            return StringWrapper()

This might seem a little weird. We're making a context manager class inside a method, just to make a single instance of it. We're relying on the `string` variable pointing to our `MutableString` instance (which is called `self` outside the class but `self` has a different meaning inside the class methods).

We could move that class outside this method instead:

    from collections.abc import MutableSequence
    from collections import UserString

    class StringWrapper:
        def __init__(self, user_string):
            self.string = user_string
        def __enter__(self):
            self.chars = list(self.string.data)
            return self.chars
        def __exit__(self, *args):
            self.string.data = "".join(self.chars)

    class MutableString(MutableSequence, UserString):
        def chars(self):
            return StringWrapper(self)
        def __setitem__(self, index, value):
            with self.chars() as chars:
                chars[index] = value
        def __delitem__(self, index):
            with self.chars() as chars:
                del chars[index]
        def insert(self, index, value):
            with self.chars() as chars:
                chars.insert(index, value)

But this could all be made a bit simpler with the `contextlib.contextmanager` decorator:

    from collections.abc import MutableSequence
    from collections import UserString
    from contextlib import contextmanager

    class MutableString(MutableSequence, UserString):
        @contextmanager
        def chars(self):
            chars = list(self.data)
            yield chars
            self.data = "".join(chars)
        def __setitem__(self, index, value):
            with self.chars() as chars:
                chars[index] = value
        def __delitem__(self, index):
            with self.chars() as chars:
                del chars[index]
        def insert(self, index, value):
            with self.chars() as chars:
                chars.insert(index, value)

I like this solution best.

It's not shorter than what we had before (we've written 5 lines of code to save 3), but I think it bundles up our `self.data`-changing logic nicely.

I hope you learned something this week about the strings, sequences, and the `collections` module.