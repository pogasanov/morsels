# Solution: Point

Hi!

If you haven't attempted to solve Point yet, close this email and go do that now before reading on. If you have attempted solving Point, read on...

This week you needed to make a class that represents a 3-dimensional point. It should have a helpful string representation and should be comparable to other points.

Here's one way we could have done this:

    class Point:

        """Three-dimensional point."""

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

        def __repr__(self):
            """Return dev-readable representation of Point."""
            return "Point(x={}, y={}, z={})".format(self.x, self.y, self.z)

        def __eq__(self, other):
            """Return True if our point is equal to the other point."""
            return self.x == other.x and self.y == other.y and self.z == other.z

That `__init__` method is our initializer. It allows our class to accept arguments as it's being constructed. We're storing those arguments on self (which is an the instance of the Point object).

The `__repr__` method is used to make a string representation of our class. This should be a programmer-readable representation of a point object. When we pass an instance of our Point class to the built-in str() or repr() functions in Python, we'll get this string representation back. Note that we're implementing `__repr__` but not `__str__` here because `__str__` defaults to `__repr__`.

That `__eq__` method is the fanciest of our three methods. It allows us to customize the behavior for == on two point objects.

By default == only answers "True" if two points are the same exact object. Our custom `__eq__` method allows us to instead answer "True" whenever the two points have the same x, y, and z attributes.

Note that we didn't make an `__ne__` method. The `__ne__` method is used to customize inequality (the != operator) and in Python 3 `__ne__` defaults to the opposite of `__eq__`. In Python 2 this is not the case, so you'd want to make a `__ne__` method.

Let's rewrite our class a bit. We're going to make a change to every method here:

    class Point:

        """Three-dimensional point."""

        def __init__(self, x, y, z):
            self.x, self.y, self.z = x, y, z

        def __repr__(self):
            """Return dev-readable representation of Point."""
            return f"Point(x={self.x}, y={self.y}, z={self.z})"

        def __eq__(self, other):
            """Return True if our point is equal to the other point."""
            return (self.x, self.y, self.z) == (other.x, other.y, other.z)

We're now using multiple assignment in `__init__`. This doesn't change the behavior but it makes it clear that x, y, and z are tied together and seen as ordered in a particular way. You may not prefer this style and that's okay, but it's possible to write your code this way if you do like it. I don't have a strong preference either way in this case.

Our `__repr__` method is quite a bit shorter now. We've decided to use f-strings (supported in Python 3.6+) instead of the string format method. This is Python's version of a "string interpolation" syntax.

The `__eq__` method has been rewritten considerably too. Before we were using 3 == signs and 2 and operators to compare corresponding x, y, and z values individually. Now we're using tuples and a single == operator to compare all 3 values as a group for each point. This is possible because tuples are compared deeply, meaning each of the items in one tuple will need to be equal for the two tuples to be seen as equal.

I particularly like the rewriting of `__eq__` here because it makes clear the order of x, y, and z and the symmetry of the two point objects. Embracing deep equality can really improve the readability of your code.

# Bonus #1

Okay let's try the first bonus now.

For the first bonus you needed to allow point objects to added to and subtracted from each other.

To do this we need to add two new methods to our Point class:

        def __add__(self, other):
            """Return copy of our point, shifted by other."""
            return Point(self.x+other.x, self.y+other.y, self.z+other.z)

        def __sub__(self, other):
            """Return copy of our point, shifted by other."""
            return Point(self.x-other.x, self.y-other.y, self.z-other.z)

We've implemented `__add__` and `__sub__` here to customize the behavior of the + and - operators on point objects. Notice that we're not modifying our own point here, but returning a new one.

It might seem like maybe there should be an easier way to do this. Maybe something like:

        def __add__(self, other):
            return self + other

But this doesn't work because this is a circular definition of the + operator. Now if we said p1 + p2, `__add__` would be called with p1 and p2 and then try to add p1 + p2 again, and then `__add__` would be called again, and so on until we got a recursion error.

We're defining what + and - even mean on point objects here.

If you don't like how long the return statement in `__add__` and `__sub__` is, you could use variables to make it shorter. For example:

        def __add__(self, other):
            """Return copy of our point, shifted by other."""
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
            return Point(x, y, z)

This is longer, but it might make things a little clearer.

Alternatively, you could keep the same code structure but make shorter variable names for x, y, and z on both self and other:

        def __add__(self, other):
            """Return copy of our point, shifted by other."""
            x1, y1, z1 = self.x, self.y, self.z
            x2, y2, z2 = other.x, other.y, other.z
            return Point(x1+x2, y1+y2, z1+z2)

Notice we're using multiple assignment again here, like we did in `__init__`. Also notice that we haven't put spaces around the + operators. It's absolutely fine to put spaces around the + operator in Python, but we already have spaces between our arguments and too many spaces can make code less readable sometimes (it can be nice to have things visually grouped together).

Regardless of what code style you choose for `__add__`, I recommend using the same style for `__sub__` since they do nearly the same thing and should look nearly the same.

# Bonus #2

Okay let's try the second bonus now.

For the second bonus we needed point objects to work with multiplication. We don't want them to be multiplied to each other though: we want them to be multiplied by a number.

We can allow the `*` operator to work on our points by implementing `__mul__`:

        def __mul__(self, scalar):
            """Return new copy of our point, scaled by given value."""
            return Point(scalar*self.x, scalar*self.y, scalar*self.z)

But this doesn't pass our tests.

This works:

    >>> p = Point(1, 2, 3)
    >>> p * 3
    Point(x=3, y=6, z=9)

But this doesn't:

    >>> p = Point(1, 2, 3)
    >>> 3 * p
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unsupported operand type(s) for *: 'int' and 'Point'

The reason this doesn't work is that `3 * p` calls `__mul__` on 3 and integers don't know how to multiply themselves by points.

Fortunately integers are a flexible object which will delegate to the object on the right-side of operators when they don't know how to work with them (they do this using [NotImplemented](https://docs.python.org/3/library/constants.html#NotImplemented)).

What this means for us is that we need to implement a `__rmul__` method to let our object know how to multiply from the right (as well as from the left).

We could do this by making an `__rmul__` method that is identical to our `__mul__` method. Or we could delegate work to our `__mul__` method:

        def __rmul__(self, scalar):
            return self.__mul__(scalar)

Note that we could return `self * scalar` here, but not `scalar * self`. It's best to return `self.__mul__(scalar)` to make it clear what we're trying to accomplish at a low level.

Also note that instead of defining a new `__rmul__` method which just calls `__mul__`, we could make a `__rmul__` variable in our class that just points directly to the `__mul__` method:

        __rmul__ = __mul__

We'd need to make sure we write that line after defining `__mul__` though.

You might be wondering why we didn't need to make `__radd__` and `__rsub__` methods. We could have done that but Python didn't require it from us because when we can only add and substract points objects from and with other point objects. Because of that symmetry, `__radd__` and `__rsub__` would never have the opportunity to be called since the left-side object is also a point and also knows how to add or subtract itself from our point.

You only need `__rmul__`, `__radd__`, and the other right-hand dunder methods when you're worried about making a particular operation work between two different objects in a **commutative** way.

# Bonus #3

Okay let's do the third bonus now.

For the third bonus we needed points to work with multiple assignment (tuple unpacking). Like this:

    >>> p = Point(1, 2, 3)
    >>> x, y, z = p

To do this we need to make our point objects into iterables. Multiple assignment loops over objects the same way "for" loops do, so if our point is iterable we'll be able to unpack it.

To make our point iterable, we need to create a `__iter__` method that returns an iterator. This method should work:

        def __iter__(self):
            return iter((self.x, self.y, self.z))

We could have made a tuple and got an iterator from it by using the built-in iter function to return.

Another way we could make a function that returns an iterator is by making a generator function:

        def __iter__(self):
            yield self.x
            yield self.y
            yield self.z

This `__iter__` method uses yield statements which will make it into a generator function. Generator functions return generators, which are iterators. So our `__iter__` method here will return an iterator as it's supposed to.

Instead of yielding each of the three values individually, we could again make a tuple and then yield from that tuple:

        def __iter__(self):
            yield from (self.x, self.y, self.z)

The "yield from" statement was added in Python 3.3\. It's essentially the same as looping over the given tuple and yielding each value individually.

All three of these approaches are reasonable. The separate yield statements is the clearest in my opinion.

Note that implementing `__iter__` on our class allows us to refactor some of our other methods in helpful ways.

Every time we do something like this:

    x, y, z = self.x, self.y, self.z

We could instead do this:

    x, y, z = self

This works because point objects are iterable now and unpacking our point using multiple assignment is just a form of iterating over it.

So we can refactor `__add__` and `__sub__` like this:

        def __add__(self, other):
            """Return copy of our point, shifted by other."""
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Point(x1+x2, y1+y2, z1+z2)

        def __sub__(self, other):
            """Return copy of our point, shifted by other."""
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Point(x1-x2, y1-y2, z1-z2)

We could also refactor `__eq__` like this if we wanted:

        def __eq__(self, other):
            """Return True if our point is equal to the other point."""
            x1, y1, z1 = self
            x2, y2, z2 = other
            return (x1, y1, z1) == (x2, y2, z2)

Or even like this:

        def __eq__(self, other):
            """Return True if our point is equal to the other point."""
            return tuple(self) == tuple(other)

I prefer the more explicit unpacking and comparison over using the tuple constructor personally. I find it a little bit easier to figure out what's going on when you glance at it.

We could also refactor `__mul__` like this:

        def __mul__(self, scalar):
            """Return new copy of our point, scaled by given value."""
            return Point(*(scalar*val for val in self))

We're using a generator expression and a `*` to unpack the generator into arguments to Point here. I find this implementation pretty confusing and I don't recommend it.

This might be reasonable though:

        def __mul__(self, scalar):
            """Return new copy of our point, scaled by given value."""
            x, y, z = self
            return Point(scalar*x, scalar*y, scalar*z)

Before we look at the last solution, I'd like to note that attempting to make an iterable `Point` by inheriting from `typing.NamedTuple` (which is useful to know about) or a class made using `collections.namedtuple` won't work for this problem because these classes create immutable objects, but we're trying to create objects that can be mutated. You can't rely on the `typing.NamedTuple` helper for this one. But you can rely on another helper: `dataclasses.dataclass`.

The last solution I'd like to discuss is one that uses Python 3.7's new `dataclasses`:

    from dataclasses import astuple, dataclass

    @dataclass
    class Point:

        """Three-dimensional point."""

        x: float
        y: float
        z: float

        def __add__(self, other):
            """Return copy of our point, shifted by other."""
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Point(x1+x2, y1+y2, z1+z2)

        def __sub__(self, other):
            """Return copy of our point, shifted by other."""
            x1, y1, z1 = self
            x2, y2, z2 = other
            return Point(x1-x2, y1-y2, z1-z2)

        def __mul__(self, scalar):
            """Return new copy of our point, scaled by given value."""
            x, y, z = self
            return Point(scalar*x, scalar*y, scalar*z)

        __rmul__ = __mul__

        def __iter__(self):
            yield from astuple(self)

We've removed our `__init__`, `__repr__`, and `__eq__` methods here and replaced them with type hints for `x`, `y`, and `z`. That `dataclass` class decorator will automatically create an initializer, string representation, and comparison methods for us based on those type hints.

The only other thing we've changed here is that our `__iter__` method uses the `astuple` helper which takes a data class and returns a tuple of its values.

If you've never played with data classes and you'd like to explore other ways to use them, check out my talk [Easier Classes: Python Classes Without All The Cruft](https://youtu.be/vD1KZgHCNCs).

Alright that's all for this week. I hope these solutions helped you think of something new!