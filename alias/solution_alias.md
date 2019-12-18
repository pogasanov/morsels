# Solution: alias

Hey!

If you haven't attempted to solve alias yet, close this email and go do that now before reading on. If you have attempted solving alias, read on...

This week you were supposed to create a helper utility that allowed the use of "alias" attributes on classes.

We could do this using Python's built-in `property` utility:

    def alias(attr):
        def getter(self):
            return eval(f'self.{attr}')
        return property(getter)

Normally we use `property` as a decorator. But decorators are callables, so we can actually call `property` just like we would with any other function.

It's similar to doing this:

    class DataRecord:
        def __init__(self, serial):
            self.serial = serial
        def title(self):
            return self.serial
        title = property(title)

Except that we're doing this dynamically and we're not hard-coding our attribute as `serial`.

Note that we're using an f-string (a Python 3.6 feature) to construct a string that includes a lookup for the correct attribute on our object and then we're using the built-in `eval` function to evaluate that string as Python code.

A safer (`eval` can be dangerous) and more clear way to do this is to use the built-in `getattr`:

    def alias(attr):
        def getter(self):
            return getattr(self, attr)
        return property(getter)

The `getattr` function allows us to look up attribute names on objects dynamically.

You might notice that we're creating that single-expression `getter` function and then referencing it just once.

We could use a `lambda` expression instead:

    def alias(attr):
        return property(lambda self: getattr(self, attr))

Python's `lambda` statement creates an _anonymous_ function (a function that doesn't have a name) inline so that we can pass it around right away without needing to create a new variable name (`getter` above) just for it. It also makes for a bit less code.

The `operator` module in the Python standard library actually contains a function that is equivalent to our `getter` function and to this `lambda` statement:

    from operator import attrgetter

    def alias(attr):
        return property(attrgetter(attr))

The `operator.attrgetter` function accepts an attribute name and returns a function that, when called with an object, will lookup that attribute on the given object.

While all of these solutions work, there is another way to solve this problem that doesn't rely on `property`.

Python's `property` utility is a [descriptor](https://docs.python.org/3/howto/descriptor.html). It's also a decorator, but the magic of `property` comes from the fact that it's a descriptor. Descriptors have a `__get__` method and they can also have a `__set__` and a `__delete__`.

We can implement `alias` as a descriptor using just a `__get__` method:

    class alias:
        def __init__(self, attr):
            self.attr = attr

        def __get__(self, obj, obj_type):
            return getattr(obj, self.attr)

When Python looks an attribute up on a class instance, it first looks on the instance and then it checks on the class. If the object it finds on the class has a `__get__` method, it knows it's a descriptor and it calls `__get__` instead of just returning the object. The descriptor protocol powers properties, instance methods, and lots of the magic you see in class-based frameworks like Django.

We'll dive deeper into descriptors in the bonuses. If you'd like to watch an hour long Python Chat I did on descriptors and properties and how attribute lookups actually work in Python, you're welcome to [watch a recording here](https://www.crowdcast.io/e/descriptors).

# Bonus 1

For the first bonus, we needed to make sure that the aliased attribute raises an exception when attempts are made to assign to it.

All of our solutions that used `property` actually pass this bonus already:

    from operator import attrgetter

    def alias(attr):
        return property(attrgetter(attr))

The reason is that the `property` descriptor implements a `__set__` that raises an exception when anyone attempts to set the attribute on instances of our class.

Here's a solution that uses just descriptors:

    class alias:
        def __init__(self, attr):
            self.attr = attr

        def __get__(self, obj, obj_type):
            return getattr(obj, self.attr)

        def __set__(self, obj, value):
            raise AttributeError("Cannot set alias")

Before we made a _non-data descriptor_ because it didn't have a `__set__`. Class instance methods are non-data descriptors.

This descriptor is a _data descriptor_ because it has a `__set__` method (even though it's one that raises an exception). Most of the uses you see for descriptors will involve data descriptors.

# Bonus 2

For the second bonus you needed to allow the `alias` class (or function if that's what you implemented it as) to accept a `write` argument.

We could actually still use `property`, like this:

    from operator import attrgetter

    def attrsetter(attr):
        def setter(obj, value):
            setattr(obj, attr, value)
        return setter

    def alias(attr, *, write=False):
        if write:
            return property(attrgetter(attr), attrsetter(attr))
        else:
            return property(attrgetter(attr))

Here when `write` is truthy, we pass a getter and a setter to the `property` descriptor (this syntax is less common than the property decorator syntax, [but it works](https://docs.python.org/3/library/functions.html#property)).

We need to make the attribute setter on our own because the `operator` module doesn't have a setter equivalent to `attrgetter`. For that, we're using `setattr`, which works like `getattr` except it takes a value to assign.

We can solve this bonus more clearly by using our descriptor class:

    class alias:
        def __init__(self, attr, *, write=False):
            self.attr = attr
            self.write = write

        def __get__(self, obj, obj_type):
            return getattr(obj, self.attr)

        def __set__(self, obj, value):
            if not self.write:
                raise AttributeError("Cannot set alias")
            setattr(obj, self.attr, value)

We're keeping track of the `write` method on our class and allowing our attribute to be set only if `write` is truthy.

Note that in both our `property`-based solution and this descriptor class one, that we're using a `*` to allow our `write` argument to only be specified as a keyword argument. This wasn't needed to pass the tests, but it disallows an unclear use of alias that relies only on positional arguments:

    title = alias('serial', True)

If you're itching to try Python 3.7's dataclasses, you could use them to implement this class also:

    from dataclasses import dataclass

    @dataclass
    class alias:

        attr: str
        write: bool = False

        def __get__(self, obj, obj_type):
            return getattr(obj, self.attr)

        def __set__(self, obj, value):
            if not self.write:
                raise AttributeError("Cannot set alias")
            setattr(obj, self.attr, value)

But this doesn't do much for us besides remove our `__init__` method. We're not able to require `write` to be a keyword only argument because that's not possible with data classes (without overriding `__init__` yourself).

# Bonus 3

For the third bonus, we were supposed to allow the `alias` descriptor to work on classes attributes (attributes that live on the class itself) as well as instance attributes (attributes that store their data on each instance individually).

This can be useful for aliasing methods that are defined on parent or child classes.

To do this we need to modify `__get__`:

    class alias:
        def __init__(self, attr, write=False):
            self.attr = attr
            self.write = write

        def __get__(self, obj, obj_type):
            if obj is None:
                return getattr(obj_type, self.attr)
            else:
                return getattr(obj, self.attr)

        def __set__(self, obj, value):
            if not self.write:
                raise AttributeError("Cannot set alias")
            setattr(obj, self.attr, value)

Our `__get__` method now checks to see if we have an instance of our object (`obj` will be `None` unless we do) and if we do, then we look up our attribute on the instance as before. Otherwise we lookup the attribute on the class itself.

I hope you had some fun practicing descriptors this week!