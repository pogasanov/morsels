# Solution: FancyReader

Hey!

If you haven't attempted to solve FancyReader yet, close this email and go do that now before reading on. If you have attempted solving FancyReader, read on...

This week you needed to make a `FancyReader` CSV reader class that acted kind of like `DictReader` but yields custom `Row` objects instead of dictionaries.

Here's one way to do this:

    import csv

    class Row:
        """Row class that stores all given arguments as attributes."""
        def __init__(self, **attrs):
            for key, value in attrs.items():
                setattr(self, key, value)

    def FancyReader(iterable, *, fieldnames, **kwargs):
        reader = csv.reader(iterable, **kwargs)
        for row in reader:
            yield Row(**dict(zip(fieldnames, row)))

We've made a generator function that uses yields `Row` objects.

Our `Row` class simply accepts all keyword arguments given to it and stores them as attributes on itself. We're using the built-in `setattr` function to set each attribute based on its name.

Here are a few neat things that are going on in our code above:

1.  We're using `**kwargs` to pass all keyword arguments given to us directly into the `reader` class (we're essentially wrapping around it)
2.  Our `Row` class simply accepts all keyword arguments given to it and stores them as attributes on itself (using the `setattr` built-in function).
3.  We're making instances of `Row` by passing the data for each row as keyword arguments (that's that odd `**dict(zip(fieldnames, row))`)

Let's talk about some other ways we could have done this.

A shorter way to assign all inputs to our `Row` initializer as attributes on our class instance is to reach into our `Row` object's `__dict__` attribute and update it directly:

    class Row:
        """Row class that stores all given arguments as attributes."""
        def __init__(self, **attrs):
            self.__dict__.update(attrs)

This is a bit more cryptic and I'm not sure I prefer it over the `for` loop with `setattr` approach.

Something to note is that we've made a generator function that is named using the camel case (`FancyReader`), which is a common class convention.

For the second and third bonus, we're going to need to make `FancyReader` generator into [an iterator class](https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/). Let's try that out now:

    class FancyReader:

        def __init__(self, iterable, *, fieldnames, **kwargs):
            self.reader = csv.reader(iterable, **kwargs)
            self.fieldnames = fieldnames

        def __next__(self):
            values = next(self.reader)
            attrs = dict(zip(self.fieldnames, values))
            return Row(**attrs)

        def __iter__(self):
            return self

Note that we've turned a 4-line generator function into a 10-line iterator class. In general, making iterator classes is more awkward than making an equivalent generator function.

We're going to go back to the generator function version of this iterator until we're forced into turning this `FancyReader` into a full iterator class.

# Bonus #1

For the first bonus, you needed to make sure your `Row` class has a nice string representation and make sure it's iterable (sort of like a tuple).

Here's one way to do that:

    class Row:

        """Row class that stores all given arguments as attributes."""

        def __init__(self, **attrs):
            for key, value in attrs.items():
                setattr(self, key, value)

        def __repr__(self):
            attrs = ", ".join(
                f"{key}={repr(value)}"
                for key, value in self.__dict__.items()
            )
            return f"Row({attrs})"

        def __iter__(self):
            yield from self.__dict__.values()

We've added a `__repr__` method for our string representation and a `__iter__` method to make our object iterable.

The `__repr__` method returns `Row(...)` where `...` is a set of comma-delimited `key=value` pairs. The values are wrapped in a `repr` call to make sure the results look like Python code: `Row(a='b')` for `a` pointing to the string `b` instead of `Row(a=b)`.

If we wanted our `Row` class to place nicely with child classes in case anyone inherits from it, we could change this:

            return f"Row({attrs})"

To this:

            return f"type(self).__name__({attrs})"

That'll make sure that child classes of `Row` use the name of their class and not the `Row` class. This isn't something that was tested for because it's sort of "going above and beyond" since we're planning for inheritance, which is a use case of `Row` that isn't necessarily expected.

Okay let's talk about that `__iter__` method. The `__iter__` method is supposed to return an iterator (see [how for loops work in Python](https://treyhunner.com/2016/12/python-iterator-protocol-how-for-loops-work/)). The easiest way to make an iterator is by making a generator function (again see my [how to make an iterator](https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/) article if you haven't yet).

We could have instead grabbed an iterator from our `__dict__` values like this:

        def __iter__(self):
            return iter(self.__dict__.values())

The first way, we're making a generator which yields each value. This way we're asking `self.__dict__` for its iterator and just returning it. Either way works.

Note that the order of attributes that we return from this iterator and the order that attributes appear in `__repr__` will only be predictably preserved if we're on Python 3.6 or higher. On older versions of Python, dictionaries were unordered. That means that instance attributes (attributes on objects) **are also unordered**.

We could try to fix this on Python 3.5 and earlier by setting `__dict__` to an `OrderedDict` object. But this won't fix a big problem: keyword arguments are passed into a dictionary which is also unordered. So we can't rely on the named argument syntax to accept our key-value pairs.

This would work on Python 3.5:

    from collections import OrderedDict
    import csv

    class Row:
        """Row class that stores all given arguments as attributes."""
        def __init__(self, attrs):
            self.__dict__ = OrderedDict(attrs)
        def __repr__(self):
            attrs = ", ".join(
                "{}={}".format(key, repr(value))
                for key, value in self.__dict__.items()
            )
            return "Row({})".format(attrs)
        def __iter__(self):
            yield from self.__dict__.values()

    def FancyReader(iterable, *, fieldnames, **kwargs):
        reader = csv.reader(iterable, **kwargs)
        for row in reader:
            yield Row(zip(fieldnames, row))

Another way to solve this problem is by throwing out our `Row` class and using `collections.namedtuple` to make a `Row` class for us:

    import csv
    from collections import namedtuple

    def FancyReader(iterable, *, fieldnames, **kwargs):
        reader = csv.reader(iterable, **kwargs)
        Row = namedtuple('Row', fieldnames)
        for row in reader:
            yield Row(*row)

This is kind of an interesting solution. We're dynamically creating a new `Row` class each time `FancyReader` is called. The `Row` class we make uses our field names as attributes names and each of our row values as the values of these attributes. Conveniently, `Row` objects have a nice string representation that matches what we're looking for and they're iterable.

I prefer this solution. I'd rather avoid writing a new class if we can have Python generate a suitable one for us.

# Bonus #2

For the second bonus you needed to make the `fieldnames` attribute optional. If `fieldnames` isn't specified, we'll consider the first row to be our field names.

This required an extra check to see if `fieldnames` wasn't specified:

    import csv
    from collections import namedtuple

    def FancyReader(iterable, *, fieldnames=None, **kwargs):
        reader = csv.reader(iterable, **kwargs)
        if fieldnames is None:
            fieldnames = next(reader)
        Row = namedtuple('Row', fieldnames)
        for row in reader:
            yield Row(*row)

If `fieldnames` is the default (we're using `None`) then we use the built-in `next` function to get the first row from our the `csv.reader` object we're wrapping around.

# Bonus #3

For the third bonus, you needed to make the `FancyReader` callable return an object that is both an iterator and has a `line_num` attribute.

For this one we finally needed to make a proper iterator class instead of creating a generator function to make an easy iterator.

Here's one version of this iterator class:

    import csv
    from collections import namedtuple

    class FancyReader:

        def __init__(self, iterable, *, fieldnames=None, **kwargs):
            self.reader = csv.reader(iterable, **kwargs)
            self.line_num = 0
            if fieldnames is None:
                fieldnames = next(self.reader)
                self.line_num += 1
            self.Row = namedtuple('Row', fieldnames)

        def __iter__(self):
            return self

        def __next__(self):
            row = self.Row(*next(self.reader))
            self.line_num += 1
            return row

We're starting that `line_num` attribute at `0` and increasing it by 1 each time we loop over our file by one more step.

Note that we're manually calling `next` on our `self.reader` object here instead of looping over it with a `for` loop. We have to do this because there's no place to put a `for` loop in an iterator class: each item that we would have `yield`-ed previously we're instead returning from our `__next__` method.

Note that our `__next__` is pretty much wrapping around the `csv.reader` object's `__next__` method because we're calling `next` on our `FancyReader` object each time we need to return a new row.

You might notice that our initializer actually consumes one row of the given iterable if no `fieldnames` attribute is given.

If we wanted to make sure we don't start looping over our file until _we're_ looper over, we could delay the creation of `self.Row` until `__next__`:

    import csv
    from collections import namedtuple

    class FancyReader:

        def __init__(self, iterable, *, fieldnames=None, **kwargs):
            self.reader = csv.reader(iterable, **kwargs)
            self.line_num = 0
            self.fieldnames = fieldnames
            self.Row = None

        def __iter__(self):
            return self

        def __next__(self):
            if self.Row is None:
                if self.fieldnames is None:
                    self.fieldnames = next(self.reader)
                    self.line_num += 1
                self.Row = namedtuple('Row', self.fieldnames)
            row = self.Row(*next(self.reader))
            self.line_num += 1
            return row

That's a bit complicated, but it makes our `FancyReader` class act a bit more like `DictReader`: nothing is looped over until someone starts looping over _us_.

I prefer this answer because this class is a bit more well-behaved than the looping-in-our-initializer version just before this.

I hope you got some good practice with iterators and classes this week!