# Solution: CyclicList

Hiya! :)

If you haven't attempted to solve CyclicList yet, close this email and go do that now before reading on. If you have attempted solving CyclicList, read on...

This week you needed to write a class, `CyclicList`, which acted sort of like a list except that looping over it resulted in an infinite loop over the same list forever.

The initial problem required only that we accept an iterable as input and that we allow looping over our `CyclicList` object (as many times as we'd like) to retrieve values from the iterable in an infinite loop.

To do this, you needed to implement both an iterable and an iterator. Here's one way to do that:

    class CyclicSequenceIterator:

        def __init__(self, sequence):
            self.sequence = sequence
            self.index = 0

        def __iter__(self):
            return self

        def __next__(self):
            value = self.sequence[self.index]
            self.index += 1
            self.index %= len(self.sequence)
            return value

    class CyclicList:

        """List-like data structure that loops in a cyclic manner."""

        def __init__(self, data):
            self.data = list(data)

        def __iter__(self):
            return CyclicSequenceIterator(self.data)

Our `CyclicList` class should be an iterable, but not an iterator. We should be able to loop over it without consuming it, just like a list, which means we can't make it an iterator.

But all iterables must implement a `__iter__` method which returns an iterator (sort of... see bonus 2). So we need to create an iterator which will accept a list and repeatedly loop over it forever. That's our `CyclicSequenceIterator` above. That `__next__` method will get called on our iterator as we loop over it.

If you've never created an iterator class before, you should try it. It's an interesting practice. But it's also rarely useful.

I noted in [my article on creating iterators](http://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/) that a better way to create an iterator is to use a generator function:

    class CyclicList:

        """List-like data structure that loops in a cyclic manner."""

        def __init__(self, data):
            self.data = list(data)

        def __iter__(self):
            i = 0
            while True:
                yield self.data[i]
                i = (i + 1) % len(self.data)

Generator functions create generators when they're called and generators are iterators. It can sometimes be useful to create an iterator class yourself, but usually when you want an iterator, you want a generator function.

The Python standard library actually includes a helper utility for creating an iterator that does just what we're looking for:

    from itertools import cycle

    class CyclicList:

        """List-like data structure that loops in a cyclic manner."""

        def __init__(self, data):
            self.data = list(data)

        def __iter__(self):
            return cycle(self.data)

So instead of making a generator function to create an iterator ourselves, we can just rely on `itertools.cycle`.

# Bonus #1

For the first bonus, we needed to make our `CyclicList` class work more like a list. We were required to allow appending and popping as well as asking for the length of our cyclic list objects.

To do this we needed to implement `__len__`, `append`, and `pop`:

    from itertools import cycle

    class CyclicList:

        """List-like data structure that loops in a cyclic manner."""

        def __init__(self, data):
            self.data = list(data)

        def __iter__(self):
            return cycle(self.data)

        def __len__(self):
            return len(self.data)

        def append(self, item):
            self.data.append(item)

        def pop(self, *args, **kwargs):
            return self.data.pop(*args, **kwargs)

We're delegating work to our inner list for each of these methods. The `pop` method accepts an optional argument, so we're just capturing all given arguments to our `pop` method and passing them onto our inner list's `pop` method.

We actually could have implemented this another way:

    class CyclicList(list):

        """List-like data structure that loops in a cyclic manner."""

        def __iter__(self):
            i = 0
            while True:
                yield self[i]
                i = (i + 1) % len(self)

Here we're inheriting from the built-in `list` type to make our class behave like a list. Then we're customizing the `__iter__` method to yield our items infinitely.

We can't use the `itertools.cycle` helper here because it would call `__iter__` on our object but we're in `__iter__` which means we'd get called again and then we'd call `cycle` again and we'd end up in an infinite recursion loop.

We could copy the contents of our list and call `cycle` on that, but there's another way to solve this problem: instead of inheriting from `list`, we could inherit from [collections.UserList](https://docs.python.org/3/library/collections.html#collections.UserList):

    from collections import UserList
    from itertools import cycle

    class CyclicList(UserList):

        """List-like data structure that loops in a cyclic manner."""

        def __iter__(self):
            return cycle(self.data)

The `UserList` class is meant for creating lists that wrap around an inner list. That's exactly what we're doing, so it's perfect for our use case.

The `__iter__` method here can cycle over our inner list (`self.data`) just fine without us accidentally calling our own `__iter__` method again.

In general, inheriting from the built-in `list` type is often a bad idea (see [my article on why inheriting from `list` is a problem](https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/)). However, in this particular problem, there's not much harm in inheriting from the built-in `list` type instead.

# Bonus #2

For the second bonus we needed to allow our `CyclicList` objects to support indexing for getting and setting items.

The `UserList` class already supports indexing, but we need cyclic indexing. We can get that by manually indexing `self.data` in a cyclic way:

    from collections import UserList
    from itertools import cycle

    class CyclicList(UserList):

        """List-like data structure that loops in a cyclic manner."""

        def __iter__(self):
            return cycle(self.data)

        def __getitem__(self, index):
            return self.data[index % len(self)]

        def __setitem__(self, index, value):
            self.data[index % len(self)] = value

If we tried this with the `list` constructor, we'd need to call `super()` to access the `list` class's version of `__getitem__` and `__setitem__`, because we don't have an inner list if we _are_ the list:

    from itertools import count

    class CyclicList(list):

        """List-like data structure that loops in a cyclic manner."""

        def __iter__(self):
            for i in count():
                yield self[i]

        def __getitem__(self, index):
            return super().__getitem__(index % len(self))

        def __setitem__(self, index, value):
            return super().__setitem__(index % len(self), value)

Note that our `__iter__` got simpler here because we can now index our list without worrying about list bounds.

Note that we could use `super().__getitem__(...)` with `UserList` as well:

    from collections import UserList
    from itertools import cycle

    class CyclicList(UserList):

        """List-like data structure that loops in a cyclic manner."""

        def __iter__(self):
            return cycle(self.data)

        def __getitem__(self, index):
            return super().__getitem__(index % len(self))

        def __setitem__(self, i, v):
            return super().__setitem__(i % len(self), v)

The `UserList` class will do the work of delegating to our inner list for us here. This approach might be slightly more pure in terms of object-oriented design, but I personally find the `self.data`-indexing approach more readable.

One more thing before we move to the next bonus: we don't necessarily need a `__iter__` method anymore!

If we're solving this using `collections.UserList` its default `__iter__` will delegate to `__getitem__` (calling it until it gets a `KeyError` which never happens here):

    from collections import UserList
    from itertools import cycle

    class CyclicList(UserList):

        """List-like data structure that loops in a cyclic manner."""

        def __getitem__(self, index):
            return super().__getitem__(index % len(self))

        def __setitem__(self, i, v):
            return super().__setitem__(i % len(self), v)

And even if we make this `CyclicList` sequence manually, we don't need a `__iter__`:

    class CyclicList:

        """List-like data structure that loops in a cyclic manner."""

        def __init__(self, data):
            self.data = list(data)

        def __len__(self):
            return len(self.data)

        def __getitem__(self, index):
            return self.data[index % len(self)]

        def __setitem__(self, index, value):
            self.data[index % len(self)] = value

        def append(self, item):
            self.data.append(item)

        def pop(self, index=-1):
            return self.data.pop(index)

This works because [defining `__getitem__` on a class makes it an iterable automatically](https://stackoverflow.com/questions/926574/why-does-defining-getitem-on-a-class-make-it-iterable-in-python#926645).

# Bonus #3

The third bonus was a bit trickier. For this one, we had to support slicing on our `CyclicList` objects.

When you slice something in Python, the `__getitem__` method is called with a `slice` object. So we need to modify our `__getitem__` method to handle slice objects specially:

        def __getitem__(self, index):
            if isinstance(index, slice):
                start = index.start
                stop = index.stop
                if start is None:
                    start = 0
                if stop is None:
                    if start >= 0:
                        stop = len(self)
                    else:
                        stop = 0
                return [self[i] for i in range(start, stop)]
            return self.data[index % len(self)]

We've added an `if` statement that figures out a range of index numbers that we should lookup when slicing our `CyclicList` objects.

Slice objects have `start`, `stop`, and `step` attributes. We're ignoring `step` and just looking at `start` and `stop` here. If either of these aren't specified (as in `my_list[:4]` or `my_list[4:]`) they'll be `None`.

We're defaulting `start` to `0` and `stop` to either the length of our list or `0`, depending on whether `start` is negative or not.

We could abstract this logic out into its own helper method:

        def _slice_indices(self, obj):
            start, stop = obj.start, obj.stop
            if obj.step is not None:
                raise ValueError("Step not supported")
            if start is None:
                start = 0
            if stop is None:
                stop = len(self) if start >= 0 else 0
            return start, stop, 1

        def __getitem__(self, index):
            if isinstance(index, slice):
                return [
                    self[i]
                    for i in range(*self._slice_indices(index))
                ]
            return self.data[index % len(self)]

This new `_slice_indices` method has an underscore before it to note, by convention, that it's an internal method. The method raises an exception if a step is given (we aren't expected to work with steps) and computes the same start and stop as before but also returns `1` as our hard-coded step.

We're using an inline `if` statement here to compute the `stop` value all on one line. I'm always torn on the readability of inline `if` statements, but I think this one fairly readable enough.

When we slice a list like this:

    >>> my_list = ['a', 'b', 'c', 'd', 'e']
    >>> my_list[-2:]
    ['d', 'e']

It's the same as passing a `slice` object directly to `__getitem__` like this:

    >>> my_list = ['a', 'b', 'c', 'd', 'e']
    >>> my_list[slice(-2, None)]
    ['d', 'e']

Normally we can call the `indices` method on slice objects by passing a length into it to compute the actual start, stop, and step of our particular list.

So given a `list` and a `slice` object, we can compute the indices to slice like this:

    >>> my_list = ['a', 'b', 'c', 'd', 'e']
    >>> my_slice = slice(-2, None)
    >>> my_slice.indices(len(my_list))
    (3, 5, 1)

That can make our math a bit simpler because it's easy to lookup index 3 to index 5 (non-inclusive) with a step of 1.

    >>> my_list[3:5:1]
    ['d', 'e']
    >>> [my_list[i] for i in range(3, 5, 1)]
    ['d', 'e']

Unfortunately can't rely on the `indices` method in our `CyclicList` object because our indices are supposed to loop around. So we've essentially implemented our own `indices` method above with `_slice_indices`.

Here's a full solution that inherits from the built-in `list` type:

    class CyclicList(list):
        def __iter__(self):
            i = 0
            while True:
                yield self[i]
                i = (i + 1) % len(self)

        def _slice_indices(self, obj):
            start, stop = obj.start, obj.stop
            if obj.step is not None:
                raise ValueError("Step not supported")
            if start is None:
                start = 0
            if stop is None:
                stop = len(self) if start >= 0 else 0
            return start, stop, 1

        def __getitem__(self, index):
            if isinstance(index, slice):
                return [
                    self[i]
                    for i in range(*self._slice_indices(index))
                ]
            return super().__getitem__(index % len(self))

        def __setitem__(self, index, value):
            super().__setitem__(index % len(self), value)

And here's a solution that inherits from `collections.UserList`:

    from collections import UserList

    class CyclicList(UserList):
        def _slice_indices(self, obj):
            start, stop = obj.start, obj.stop
            if obj.step is not None:
                raise ValueError("Step not supported")
            if start is None:
                start = 0
            if stop is None:
                stop = len(self) if start >= 0 else 0
            return start, stop, 1

        def __getitem__(self, index):
            if isinstance(index, slice):
                return [
                    self[i]
                    for i in range(*self._slice_indices(index))
                ]
            return self.data[index % len(self)]

        def __setitem__(self, index, value):
            self.data[index % len(self)] = value

Note that we no longer have a `__iter__` method here! The reason is that `collections.UserList` implements `__iter__` by calling just `__getitem__` repeatedly until a `KeyError` is raised (this is similar to how sequences that don't implement `__iter__` at all work).

You could also inherit from `collections.abc.MutableSequence` to solve this one, but that'd take a little bit more work.

    from collections.abc import MutableSequence

    class CyclicList(MutableSequence):

        def __init__(self, data):
            self.data = list(data)

        def _slice_indices(self, obj):
            start, stop = obj.start, obj.stop
            if obj.step is not None:
                raise ValueError("Step not supported")
            if start is None:
                start = 0
            if stop is None:
                stop = len(self) if start >= 0 else 0
            return start, stop, 1

        def __getitem__(self, index):
            if isinstance(index, slice):
                return [
                    self[i]
                    for i in range(*self._slice_indices(index))
                ]
            return self.data[index % len(self)]

        def __setitem__(self, index, value):
            self.data[index % len(self)] = value

        def __delitem__(self, index):
            del self.data[index % len(self)]

        def __len__(self):
            return len(self.data)

        def insert(self, index, value):
            self.data.insert(index, value)

My favorite solution is that `UserList` solution above.

I hope you got some good practice with creating your own list-wrapping objects this week. It really doesn't take too much code to make your own data structures sometimes!