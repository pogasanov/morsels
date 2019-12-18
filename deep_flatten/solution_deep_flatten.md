# Solution: deep_flatten

Hey!

If you haven't attempted to solve deep_flatten yet, close this email and go do that now before reading on. If you have attempted solving deep_flatten, read on...

This week you were supposed to make a deep_flatten function which "flattened" a deeply nested iterable of iterables.

At first our function was only expected to work with lists and tuples. We could solve the base problem like this:

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        flattened = []
        for item in iterable:
            if type(item) in [list, tuple]:
                for x in deep_flatten(item):
                    flattened.append(x)
            else:
                flattened.append(item)
        return flattened

Here we're creating an empty list, looping over each item in our iterable, and then handling two cases: the case when our item is a list or a tuple and the case where it is not.

When we encounter a list or tuple, we call deep_flatten on the item and loop over the results, appending each to our new list. When the item is not a list or a tuple, we simply append it to our new list.

This is a classic example of recursion (our function calling itself). Recursion often makes sense when you're working with a nested structure of unknown depth that you need to traverse.

That type(item) check may stand out as problematic. If we encountered a sub- class of list or a sub-class of tuple ([collections.namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple) for example) our function wouldn't flatten those types.

We should instead be doing an isinstance check, to allow for inheritance from list and tuple:

            if isinstance(item, (list, tuple)):
                for x in deep_flatten(item):
                    flattened.append(x)

The isinstance function accepts an object and a tuple of types and will return True if that object's class inherits from any of those types.

You might also notice that our "for" loop with an append could also be simplified using the list extend method:

            if isinstance(item, (list, tuple)):
                flattened.extend(deep_flatten(item))

Our full solution looks like this:

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        flattened = []
        for item in iterable:
            if isinstance(item, (list, tuple)):
                flattened.extend(deep_flatten(item))
            else:
                flattened.append(item)
        return flattened

Before we move to the bonus, I'd like to take a look at a non-recursive solution to this problem.

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        flattened = []
        items = list(iterable)
        while items:
            item = items.pop()
            if isinstance(item, (list, tuple)):
                items.extend(item)
            else:
                flattened.insert(0, item)
        return flattened

In this non-recursive solution, we're copying our iterable into a new list (so we don't have to be afraid of mutating it and upsetting someone). Then we loop over this new list until it's empty.

Every iteration of our loop, we pop an item from the end of our items list. Then we check whether the item is a list or a tuple. If it is, we extend our items list with the items in this list/tuple. If it's not, then we insert the item to the beginning of our flattened list.

We have to insert the item to the beginning of our list because if we insert to the end, we'll end up with our all our items in reverse order. But inserting to the beginning of a list is a very expensive operation (it requires shuffling every item over to make room for the new item).

We could instead append to the end of our new list and then reverse it afterward:

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        flattened = []
        items = list(iterable)
        while items:
            item = items.pop()
            if isinstance(item, (list, tuple)):
                items.extend(item)
            else:
                flattened.append(item)
        return reversed(flattened)

Or we could use a deque, a double-ended queue, from the collections module. A deque object allows inserting items at the end or beginning of the queue inexpensively (constant time, O(1)).

    from collections import deque

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        flattened = deque()
        items = list(iterable)
        while items:
            item = items.pop()
            if isinstance(item, (list, tuple)):
                items.extend(item)
            else:
                flattened.appendleft(item)
        return flattened

Sometimes recursion can make code overly complicated, but I think in this case our recursive solution was more clear than this iterative solution.

# Bonus #1

For the first bonus we were supposed to make our deep_flatten function work with other iterables besides lists and tuples.

Currently we're manually type-checking our items to see whether they inherit from list or tuple.

We could instead use exception handling to determine whether our items are iterable:

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        flattened = []
        for item in iterable:
            try:
                flattened.extend(deep_flatten(item))
            except TypeError:
                flattened.append(item)
        return flattened

Here we're attempting to call deep_flatten on item, which will iterate over it. If that fails with a TypeError, our item is not an iterable.

Exception handling can be a bit costly CPU-wise. We could instead continue type-checking but look for collections.abc.Iterable instead of list and tuple:

    from collections.abc import Iterable

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        flattened = []
        for item in iterable:
            if isinstance(item, Iterable):
                flattened.extend(deep_flatten(item))
            else:
                flattened.append(item)
        return flattened

Iterable is an abstract base class that can be used for creating your own iterable easily, but the Iterable class also overrides isinstance and issubclass checks so that any object that has a `__iter__` method will return True when the question isinstance(my_object, Iterable) is asked.

So we're type checking here, but we're still practicing duck typing. I discussed how this is the case in [this question during a chat I did on duck typing](https://www.crowdcast.io/e/duck-typing-2/1/q/-LEgPfNJ1UeW_BhSpcN2).

Another way to check for iterability is to directly look for a `__iter__` attribute:

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        flattened = []
        for item in iterable:
            if hasattr(item, '__iter__'):
                flattened.extend(deep_flatten(item))
            else:
                flattened.append(item)
        return flattened

This is what isinstance(item, Iterable) is doing under the hood. But I find this hasattr check a bit less descriptive, so I prefer the isinstance check personally.

# Bonus #2

For the second bonus we were supposed to make our function return an iterator.

The easiest way to do that is to turn our function into a generator function:

    from collections.abc import Iterable

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        for item in iterable:
            if isinstance(item, Iterable):
                for x in deep_flatten(item):
                    yield x
            else:
                yield item

When creating a generator function from a function that returns a list, you can usually replace all append calls with a yield and then remove the return of the list and the list itself.

In this case we expanded that extend call into a "for" loop that yields.

Since our loop just yields, we can use "yield from" instead:

    from collections.abc import Iterable

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        for item in iterable:
            if isinstance(item, Iterable):
                yield from deep_flatten(item)
            else:
                yield item

The "yield from" statement is to a list extend the way a "yield" statement is to a list append.

# Bonus #3

For the third bonus we were supposed to make our deep_flatten function work with strings.

The problem with strings is that they're infinitely recursive. Python doesn't have a character type, which usually makes things easier but in this particular case it complicates things for us a bit. Strings contain strings which contain strings and so on.

    >>> x = "hello"
    >>> x[0]
    'h'
    >>> x[0][0]
    'h'
    >>> x[0][0][0]
    'h'

We could modify our function to handle strings specially:

    from collections.abc import Iterable

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        for item in iterable:
            if isinstance(item, (str, bytes)):
                yield item
            elif isinstance(item, Iterable):
                yield from deep_flatten(item)
            else:
                yield item

We could collapse that if-elif-else into just an if-else:

    from collections.abc import Iterable

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        for item in iterable:
            if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
                yield from deep_flatten(item)
            else:
                yield item

This isn't terribly elegant, but there's not really a great way to handle strings when flattening.

So that's my preferred solution. I'd like to show off a few more non- recursive solutions that work for all three bonuses before we wrap up.

Here's a long one:

    from collections.abc import Iterable

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        iterators = [iter(iterable)]
        while iterators:
            iterator = iterators[-1]
            iterator_found = False
            while not iterator_found:
                try:
                    item = next(iterator)
                except StopIteration:
                    iterators.pop()
                    break
                if (isinstance(item, Iterable)
                        and not isinstance(item, (str, bytes))):
                    iterators.append(iter(item))
                    iterator_found = True
                    break
                else:
                    yield item

We're maintaining a list of iterators here. We're maintaining a stack of iterators. We yielding non-iterable items as they're found in our current iterator. As we find iterables, we append them to the end of our iterators list and move to working with them instead. Once iterators are exhausted, we remove them from our iterators list until there are no more iterators left.

A non-recursive solution to deep_flatten pretty much has to maintain some sort of iterators queue.

Here's version of the same algorithm that doesn't manually call the next function:

    from collections.abc import Iterable

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        iterators = [iter(iterable)]
        while iterators:
            was_flat = True
            for item in iterators[-1]:
                if (isinstance(item, Iterable)
                        and not isinstance(item, (str, bytes))):
                    iterators.append(iter(item))
                    was_flat = False
                    break
                else:
                    yield item
            if was_flat:
                iterators.pop()

We're using a "for" loop here instead of calling next manually.

That was_flat variable is essentially the opposite of our iterator_found variable from before.

There's a Python construct that we can use to remove the need for that was_flat variable. We can use for-else here:

    from collections.abc import Iterable

    def deep_flatten(iterable):
        """Flatten an iterable of iterables."""
        iterators = [iter(iterable)]
        while iterators:
            for item in iterators[-1]:
                if (isinstance(item, Iterable)
                        and not isinstance(item, (str, bytes))):
                    iterators.append(iter(item))
                    break
                else:
                    yield item
            else:  # nobreak
                iterators.pop()

The else clause on "for" loops is a construct I always forget about and I'm pretty sure most Python programmers forget about it as well.

That "else" keyword on a "for" loop is a little weird to see. Ned Batchelder has a [blog post that explains for/else](https://nedbatchelder.com/blog/201110/forelse.html) that I'd recommend.

You may notice that I put a "nobreak" comment there. Some people think Python should have added another keyword "nobreak", which would have made that construct more clear than for-else. For Python programmers unfamiliar with this construct, I think a comment helps a bit at explaining it.

I hope you learned something new this week!