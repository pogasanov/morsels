# Solution: Vector

Hey!

If you haven't attempted to solve Vector yet, close this email and go do that now before reading on. If you have attempted solving Vector, read on...

This week you needed to make a `Vector` class which has `x`, `y`, and `z` attributes. The class was supposed to quite a few basic operations beyond just having these attributes.

It needed to support equality and inequality and the vector needed to work with tuple unpacking. It also needed to use `__slots__` to store its attributes instead of having a less memory efficient `__dict__` dictionary.

Here's one solution:

    class Vector:

        __slots__ = 'x', 'y', 'z'

        def __init__(self, x, y, z):
            self.x, self.y, self.z = x, y, z

        def __iter__(self):
            yield self.x
            yield self.y
            yield self.z

        def __eq__(self, other):
            return tuple(self) == tuple(other)

In our initializer we're assigning to `self.x`, `self.y`, and `self.z`. We're doing it on a single line of code, using [tuple unpacking](https://treyhunner.com/2018/03/tuple-unpacking-improves-python-code-readability/), but we could have done it with three separate assignment statements if we wanted.

That `__slots__` at the top of our class ensures that our class doesn't use a dictionary to store whatever arbitrary attributes we want to store on our vector objects. Instead we use a tuple of exactly the three attributes we'd like each vector to include. This is usually done to save memory (if you have one million class instances, a tuple for each is much less memory intensive than a dictionary for each).

We have a `__iter__` method because our `Vector` class needs to work with multiple assignment, which means it needs to be iterable. The `__iter__` method must return an iterator. I wrote an article explaining that [the easiest way to make an iterator is to make a generator][making generator], and that's exactly what we're doing here. those `yield` statements magically turn this into a generator function (or generator method since this function is also a method on our class).

The `__eq__` method powers equality, so when we ask whether two vectors are equal (using `==`) that method will be called. This method also gives us inequality (`!=`) automatically because the default `__ne__` just negates whatever `__eq__` returns.

We're sort of cheating here by converting each of our vector objects to tuples (which we can do because we have a `__iter__` so we can iterate over them) and then comparing them. We could have instead compared the coordinates in each of the two vectors (e.g. `self.x` and `other.x`) individually. Personally I prefer to delegate to our `__iter__` method and convert our vectors to tuples to compare them.

Note that we should really be confirming that we're actually comparing vectors here. Currently we get odd behavior like this:

    >>> Vector(1, 2, 3) == [1, 2, 3]
    True

To ensure we only allow equality for other vectors, we can do this:

        def __eq__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            return tuple(self) == tuple(other)

Our tests weren't actually checking for that though.

You might have thought, we could use a named tuple for this!

Python 2 had a `collections.namedtuple` class factory function. Python 3.5 introduced a `typing.NamedTuple` base class for making tuple-like objects.

You may have tried something like this:

    from typing import NamedTuple

    class Vector(NamedTuple):
        x: float
        y: float
        z: float

This actually passes all of our tests, except for one. The test that fails checks to ensure our class doesn't do odd things that it shouldn't do, like these things:

    >>> Vector(1, 2, 3) + Vector(4, 5, 6)
    (1, 2, 3, 4, 5, 6)
    >>> Vector(4, 5, 6) < Vector(6, 5, 4)
    True
    >>> len(Vector(1, 2, 3))
    3

I did a talk on this recently called [Easier Classes](https://www.youtube.com/watch?v=COMRNKAVesI), during which I talked about how `NamedTuple` shouldn't be used unless you're trying to make a class that should act just like a tuple does.

Instead, we could use `dataclasses`:

    from dataclasses import astuple, dataclass

    @dataclass
    class Vector:

        x: float
        y: float
        z: float

        __slots__ = 'x', 'y', 'z'

        def __iter__(self):
            yield from astuple(self)

The `dataclasses` library is included in Python 3.7, but if you're on an earlier version of Python 3, you could use it as a third-party library also by installing it with `pip install dataclasses`.

Here we're decorating our class with the `dataclass` _class decorator_. That will read those three type hints we defined (e.g. `x: float`) and automatically create an initializer, equality method, and a nice string representation.

We still have to specify `__slots__` ourself and we still have to make our own `__iter__` method. Note that we're using `astuple` to convert our data class to a tuple and then we're using a `yield from` statement to loop over it and yield each of the three coordinates individually.

I prefer the dataclass approach to this problem. The manual implementation isn't too bad, but data classes really remove a lot of the boilerplate code.

# Bonus #1

For the first bonus, we needed to make our vectors _shiftable_, meaning we can use `+` and `-` to add and subtract them from each other.

Regardless of the way we solve our initial problem, we should be able to solve this one by creating `__add__` and `__sub__` methods like this:

        def __add__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            return Vector(*(a + b for a, b in zip(self, other)))

        def __sub__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            return Vector(*(a - b for a, b in zip(self, other)))

These two methods do nearly the same thing, but with the operator changed.

Each is returning `NotImplemented` when given a non-vector in order to make sure we can't add tuples and other iterables to our vector class.

We're zipping together our vector and the other vector so that we can loop over the coresponding coordinates in each and add or subtract them from each other. We're making a generator expression to get those three new coordinates and then immediately unpacking it (using `*`) to construct a new vector with those new `x`, `y`, and `z` values.

We could have instead wrote:

        def __add__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            x, y, z = (a + b for a, b in zip(self, other))
            return Vector(x, y, z)

Which is a little more explicit.

If we wanted to be even more explicit, we could have done this:

        def __add__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            return Vector(self.x+other.x, self.y+other.y, self.z+other.z)

Or better yet, we could have unpacked the three coordinates for each point like this:

        def __add__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Vector(x1+x2, y1+y2, z1+z2)

We're relying on the fact that our vector objects are iterable here to unpack their values into nicely named variables so that we can then add those values together.

I prefer the last approach the most, followed by the first approach. The last approach here is the most readable and most explicit. The first approach (the `*` and `zip` one) is the most generic because it would work for any number of attributes. We don't need generic, since we know our class only has three coordinates, so let's choose the last approach.

Our class looks like this now:

    from dataclasses import astuple, dataclass

    @dataclass
    class Vector:

        x: float
        y: float
        z: float

        __slots__ = 'x', 'y', 'z'

        def __iter__(self):
            yield from astuple(self)

        def __add__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Vector(x1+x2, y1+y2, z1+z2)

        def __sub__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Vector(x1-x2, y1-y2, z1-z2)

# Bonus #2

For the second bonus, we needed to be able to scale our vectors by a number, meaning we needed to support multiplication with numbers and division by numbers.

This one was tricky for a few reasons. First we needed to support right-hand and left-hand multiplication. Second we needed to make sure we were multiplying by a number and not a string or something else.

Here's one way to do just multiplication:

    from numbers import Number

    class Vector:
        # ...
        def __mul__(self, scalar):
            if not isinstance(scalar, Number):
                return NotImplemented
            return Vector(*(scalar * a for a in self))
        def __rmul__(self, scalar):
            return self.__mul__(scalar)

Note that we're creating a `__mul__` method as well as a `__rmul__` metod here. The `__mul__` method is needed for left-hand multiplication (`vector * 3`) and `__rmul__` is needed for right-hand multiplication (`3 * vector`).

Since these should do the same thing, we could just write this:

    from numbers import Number

    class Vector:
        # ...
        def __mul__(self, scalar):
            if not isinstance(scalar, Number):
                return NotImplemented
            return Vector(*(scalar * a for a in self))
        __rmul__ = __mul__

We're pointing a our `__rmul__` class attribute to the same function as our `__mul__` class attribute, so they'll both be the exact same method.

Note that we're doing an isinstance check on `numbers.Number`. We could have said `isinstance(scalar, (float, int))`, but there are other types of numbers (`Decimal`, `complex`) and we don't necessarily want to limit ourselves to just one type of number for this operation.

For division, we could use `__truediv__`:

        def __truediv__(self, scalar):
            if not isinstance(scalar, Number):
                return NotImplemented
            return Vector(*(a / scalar for a in self))

We've been using generator expressions here, which isn't the most readable. Let's combine these methods into our class and drop the slightly crytic generator expressions:

    from dataclasses import astuple, dataclass
    from numbers import Number

    @dataclass
    class Vector:

        x: Number
        y: Number
        z: Number

        __slots__ = 'x', 'y', 'z'

        def __iter__(self):
            yield from astuple(self)

        def __add__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Vector(x1+x2, y1+y2, z1+z2)

        def __sub__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Vector(x1-x2, y1-y2, z1-z2)

        def __mul__(self, scalar):
            if not isinstance(scalar, Number):
                return NotImplemented
            x, y, z = self
            return Vector(scalar*x, scalar*y, scalar*z)
        __rmul__ = __mul__

        def __truediv__(self, scalar):
            if not isinstance(scalar, Number):
                return NotImplemented
            x, y, z = self
            return Vector(x/scalar, y/scalar, z/scalar)

Note that we're relying on tuple unpacking more here (I really do think [it makes code easier to read](https://treyhunner.com/2018/03/tuple-unpacking-improves-python-code-readability/)) and we've made the type hints for our data attributes more generic by changing them from `float` to `Number`.

# Bonus #3

The last bonus was tricky if you weren't using dataclasses.

For the last bonus we had to make sure our vector objects were immutible (meaning we couldn't change their coordinates after they'd been made).

Without data classes, we'd need to override `__setattr__` to raise an error (not `__setattribute__` which does something a bit different and more generic):

        def __setattr__(self, name, value):
            raise AttributeError("Vectors are immutable")

But then our initializer would fail when we try to assign attributes (e.g. `self.x = x`), so we'd need to manually call our parent class's `__setattr__` method to force an assignment of the attributes:

        def __init__(self, x, y, z):
            super().__setattr__('x', x)
            super().__setattr__('y', y)
            super().__setattr__('z', z)

If we're using dataclasses, we could instead modify our `@dataclass` class decorator to look like this:

    @dataclass(frozen=True)

My preferred implementation looks like this:

    from dataclasses import astuple, dataclass
    from numbers import Number

    @dataclass(frozen=True)
    class Vector:

        x: Number
        y: Number
        z: Number

        __slots__ = 'x', 'y', 'z'

        def __iter__(self):
            yield from astuple(self)

        def __add__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Vector(x1+x2, y1+y2, z1+z2)

        def __sub__(self, other):
            if not isinstance(other, Vector):
                return NotImplemented
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Vector(x1-x2, y1-y2, z1-z2)

        def __mul__(self, scalar):
            if not isinstance(scalar, Number):
                return NotImplemented
            x, y, z = self
            return Vector(scalar*x, scalar*y, scalar*z)
        __rmul__ = __mul__

        def __truediv__(self, scalar):
            if not isinstance(scalar, Number):
                return NotImplemented
            x, y, z = self
            return Vector(x/scalar, y/scalar, z/scalar)

A more compact implementation of this class, looks like this:

    from dataclasses import astuple, dataclass
    from numbers import Number
    @dataclass(frozen=True)
    class Vector:
        x: Number
        y: Number
        z: Number
        __slots__ = 'x', 'y', 'z'
        def __iter__(self): yield from astuple(self)
        def __add__(self, other):
            if not isinstance(other, Vector): return NotImplemented
            return Vector(*(a + b for a, b in zip(self, other)))
        def __sub__(self, other):
            if not isinstance(other, Vector): return NotImplemented
            return Vector(*(a - b for a, b in zip(self, other)))
        def __mul__(self, scalar):
            if not isinstance(scalar, Number): return NotImplemented
            return Vector(*(scalar * a for a in self))
        __rmul__ = __mul__
        def __truediv__(self, scalar):
            if not isinstance(scalar, Number): return NotImplemented
            return Vector(*(a / scalar for a in self))

That's half as many lines of code but it's also considerable less readable. Please don't write code like that.

I hope you learned something new about Python's class system this week. If so, write it down so you can remember it later!