# Solution: cd

Hey!

If you haven't attempted to solve cd yet, close this email and go do that now before reading on. If you have attempted solving cd, read on...

This week you needed to make a context manager (called `cd`) which temporarily changed directories.

Here's one way to do this:

    import os

    class cd:

        """Context manager that temporarily changes directories."""

        def __init__(self, directory):
            self.directory = directory

        def __enter__(self):
            self.original = os.getcwd()
            os.chdir(self.directory)

        def __exit__(self, exc, value, tb):
            os.chdir(self.original)

Context managers work via a `__enter__` method (which is called when the `with` block is entered) and a `__exit__` method (which is called when the `with` block is exited).

Our context manager changes directories in the `__enter__` block instead of in `__init__` because we want this case to work properly:

    dirs = cd(some_directory)
    print("Directory hasn't changed yet")
    with dirs:
        print("Directory has changed in here though")

Note that we also need to store the original directory that we changed from and then change back to it in `__exit__`.

We also could have solved this with the `contextlib.contextmanager` decorator:

    from contextlib import contextmanager
    import os

    @contextmanager
    def cd(directory):
        """Context manager that temporarily changes directories."""
        original = os.getcwd()
        os.chdir(directory)
        try:
            yield
        finally:
            os.chdir(original)

The `contextmanager` decorator is a clever (and sort of weird) helper that allows us to create a one-yield generator function that acts as a context manager.

Both of these solutions will seem weird and new to folks who've never created a context manager themselves, but I think this second one is a bit clearer.

I prefer this solution because the state maintenance is easy (no `self.directory` and `self.original` to worry about) and the code looks sort of like what it does (that `try-finally` syntax is likely more familiar than `__exit__` is).

# Bonus #1

For the first bonus you needed to create a temporary directory to change into if no directory was specified.

Here's one way to do that:

    from contextlib import contextmanager
    import os
    from shutil import rmtree
    from tempfile import mkdtemp

    @contextmanager
    def cd(directory=None):
        """Context manager that temporarily changes directories."""
        original = os.getcwd()
        if directory is None:
            tmpdir = directory = mkdtemp()
        else:
            tmpdir = None
        os.chdir(directory)
        try:
            yield
        finally:
            os.chdir(original)
            if tmpdir:
                rmtree(tmpdir)

We're relying on `tempfile.mkdtemp` to create a temporary directory for us. The `mkdtemp` function won't automatically delete this directory for us, so we're doing that ourselves using `rmtree` in our `finally` block.

We could instead use the `tempfile.TemporaryDirectory` context manager, which clean up that temporary directory automatically on exit:

    from contextlib import contextmanager
    import os
    from tempfile import TemporaryDirectory

    @contextmanager
    def cd(directory=None):
        """Context manager that temporarily changes directories."""
        original = os.getcwd()
        with TemporaryDirectory() as tmpdir:
            if directory is None:
                directory = tmpdir
            os.chdir(directory)
            try:
                yield
            finally:
                os.chdir(original)

We've put a context manager inside of our context manager.

One thing that's a little odd here is that we're _always_ creating a temporary directory now, even when a directory is specified.

It's a little tricky to fix that without duplicating our whole `try-finally` block.

Here's one way we could avoid creating a temporary directory if we don't need to:

    from contextlib import contextmanager
    import os
    from tempfile import TemporaryDirectory

    @contextmanager
    def cd(path=None):
        """Context manager that temporarily changes directories."""
        cm = TemporaryDirectory() if path is None else nullcontext(path)
        with cm as directory:
            original = os.getcwd()
            os.chdir(directory)
            try:
                yield
            finally:
                os.chdir(original)

    @contextmanager
    def nullcontext(return_value=None):
        yield return_value

Here we've create a `nullcontext` context manager that does nothing except for return the given `path` object when entered.

This allows us to conditionally create and use either this `nullcontext` "dummy" context manager or the `TemporaryDirectory` context manager.

Python 3.7 actually added a `nullcontext` context manager that does exactly the same thing as ours. So we could delete ours and change that first `import` statement to import the Python 3.7 one instead:

    from contextlib import contextmanager, nullcontext

# Bonus #2

For the second bonus your context manager, when entered, needed to return an object with `previous` and `current` attributes.

Here's one way we could have done that:

    from contextlib import contextmanager, nullcontext
    import os
    from tempfile import TemporaryDirectory
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class Dir:
        previous: os.PathLike
        current: os.PathLike

    @contextmanager
    def cd(path=None):
        """Context manager that temporarily changes directories."""
        cm = TemporaryDirectory() if path is None else nullcontext(path)
        with cm as directory:
            original = os.getcwd()
            os.chdir(directory)
            try:
                yield Dir(original, directory)
            finally:
                os.chdir(original)

That `dataclass` decorator only works in Python 3.7. If you're curious about it, see [my talk on dataclasses (and more)](https://www.youtube.com/watch?v=vD1KZgHCNCs).

Our context manager is starting to grow out of the `contextmanager` decorator. It's time to start manually using the class-syntax again:

    import os
    from tempfile import TemporaryDirectory

    class cd:

        """Context manager that temporarily changes directories."""

        def __init__(self, directory=None):
            self.current = directory
            self.tmpdir = None

        def __enter__(self):
            if self.current is None:
                self.tmpdir = TemporaryDirectory()
                self.current = self.tmpdir.name
            self.previous = os.getcwd()
            os.chdir(self.current)
            return self

        def __exit__(self, *args):
            os.chdir(self.previous)
            if self.tmpdir:
                self.tmpdir.cleanup()

Here we're returning _our own_ object from our `__enter__` method (with `return self`) and hanging `current` and `previous` attributes off of us. This is a pretty common thing to do: you'll likely see `return self` at the end of the `__enter__` in other context managers. This is how the built-in `open` context manager works (though it's not how `TemporaryDirectory` works (it returns the path as a string).

Here's another similar solution:

    from contextlib import nullcontext
    import os
    from tempfile import TemporaryDirectory

    class cd:

        """Context manager that temporarily changes directories."""

        def __init__(self, path=None):
            self.tmpdir = nullcontext(path) if path else TemporaryDirectory()

        def __enter__(self):
            self.current = self.tmpdir.__enter__()
            self.previous = os.getcwd()
            os.chdir(self.current)
            return self

        def __exit__(self, exc, value, tb):
            os.chdir(self.previous)
            self.tmpdir.__exit__(exc, value, tb)

Here we're using that `nullcontext` trick we used before to create one of two context managers that we're wrapping around: either `TemporaryDirectory` (which creates a temporary directory) or `nullcontext` (which does nothing).

We're manually calling `__enter__` and `__exit__` on this context manager we're wrapping around.

Note that this actually creates the temporary directory in our initializer (not in `__enter__`) because that's how `TemporaryDirectory` works. This is probably fine for our use case.

We could have been a bit less explicit in our `__exit__` method by capturing and passing on all the positional arguments given to us (which will be `None` unless an exception occurred):

        def __exit__(self, *args):
            os.chdir(self.previous)
            self.tmpdir.__exit__(*args)

As much as I dislike duplicating unused code, explicit is better implicit and it might be best to be explicit in this case just in case.

I'm not sure whether this `nullcontext` solution is overly clever or just clever enough. I find it somewhat elegant in the way it removed all the conditional statements from our `__enter__` and `__exit__` methods, but it might be a little tricky for a newcomer to understand. Then again the code we had before was a bit tricky as well.

Personally I'd probably opt for this solution.

# Bonus #3

For the third bonus you needed to add `enter` and `exit` methods to `cd` objects.

There's really no nice way to solve this one using `contextlib.contextmanager` because the context manager returned won't be able to have any extra methods.

We could just add these two methods to delegate to our `__enter__` and `__exit__` methods:

        def enter(self):
            self.__enter__()

        def exit(self):
            self.__exit__(None, None, None)

Note that we'll actually need to specify our `__exit__` methods manually in this case because `TemporaryDirectory` expects all three of those arguments.

If we wanted to remove that awkward `None, None, None` we could make our `__exit__` method have default values:

        def __exit__(self, exc=None, value=None, tb=None):
            os.chdir(self.previous)
            self.tmpdir.__exit__(exc, value, tb)

We could instead solve this bonus by flipping things around and having `enter` and `exit` do the actual work:

    from contextlib import nullcontext
    import os
    from tempfile import TemporaryDirectory

    class cd:

        """Context manager that temporarily changes directories."""

        def __init__(self, path=None):
            self.tmpdir = nullcontext(path) if path else TemporaryDirectory()

        def enter(self):
            self.current = self.tmpdir.__enter__()
            self.previous = os.getcwd()
            os.chdir(self.current)

        def exit(self):
            os.chdir(self.previous)
            self.tmpdir.__exit__(None, None, None)

        def __enter__(self):
            self.enter()
            return self

        def __exit__(self, *args):
            self.exit()

Here our `__enter__` and `__exit__` methods just wrap around our `enter` and `exit` methods.

We do need to pass the awkward `None, None, None` arguments to `self.tmpdir` for this to work, but I don't find that too awkward.

I find both of these solutions perfectly fine. It really depends on how you want to see the world: is the context manager behavior the primary behavior or is the manual `enter`/`exit` calling the primary behavior?

I hope you learned something new this week!