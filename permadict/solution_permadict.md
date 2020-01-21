# Solution: PermaDict

Hey,

If you haven't attempted to solve PermaDict yet, close this email and go do that now before reading on. If you have attempted solving PermaDict, read on...

This week you were supposed to create a dictionary-like class that didn't allow keys to have their values updated once they'd be set.

Here's one solution:

    class PermaDict(dict):

        """Mapping that doesn't allow updating keys once set."""

        def __setitem__(self, key, value):
            if key in self:
                raise KeyError(f"{key} already in dictionary.")
            return super().__setitem__(key, value)

        def update(self, other=None, **kwargs):
            if isinstance(other, dict):
                for key, value in other.items():
                    self[key] = value
            elif other is not None:
                for key, value in other:
                    self[key] = value
            for key, value in kwargs.items():
                self[key] = value

Here we're inheriting from the dict class. We're doing this so that we don't have to manually implement all of the methods that dictionaries normally have.

We're overriding the `__setitem__` method in our class to disallow setting keys that are already in our dictionary.

We also need a custom update method for our tests to pass. The reason is that the dictionary update method hard-codes the setting of keys. It doesn't delegate work to `__setitem__`.

In our update method we have to accept dictionaries, lists of 2-tuples, and keyword arguments. We have an if-elif for the single positional argument that update accepts. Then we loop over the given keyword arguments to set those in our dictionary as well.

We've implemented the update method this way because this is how Python's dictionary update method works and we need to re-implement that functionality in our class.

If we'd decided to practice composition instead of inheritance here, we'd need to implement a lot more methods:

    class PermaDict:

        """Mapping that doesn't allow updating keys once set."""

        def __init__(self, *args, **kwargs):
            self.data = dict(*args, **kwargs)

        def __iter__(self):
            return iter(self.data)

        def __len__(self):
            return len(self.data)

        def __getitem__(self, key):
            return self.data[key]

        def pop(self, key):
            return self.data.pop(key)

        # ...

We'd need to support the `__iter__`, `__len__`, keys, values, items, pop, `__getitem__`, and `__eq__` methods... and anything else that might reasonably be expected of our dictionary-like class.

If we did choose this route, we could get quite a bit of this functionality for free by inheriting from the Mapping abstract base class in the collections.abc module:

    from collections.abc import Mapping

    class PermaDict(Mapping):

        """Mapping that doesn't allow updating keys once set."""

        def __init__(self, *args, **kwargs):
            self.data = dict(*args, **kwargs)

        def __iter__(self):
            return iter(self.data)

        def __len__(self):
            return len(self.data)

        def __getitem__(self, key):
            return self.data[key]

        def __setitem__(self, key, value):
            if key in self:
                raise KeyError(f"{key} already in dictionary.")
            self.data[key] = value

        def update(self, other=None, **kwargs):
            if isinstance(other, dict):
                for key, value in other.items():
                    self[key] = value
            elif other is not None:
                for key, value in other:
                    self[key] = value
            for key, value in kwargs.items():
                self[key] = value

        def pop(self, key):
            return self.data.pop(key)

To create a Mapping, we need to implement `__iter__`, `__len__`, `__getitem__`, `__setitem__`, and update. Our mapping will implement the rest of our methods for us... sort of. We don't get setdefault, copy, and some other less critical dictionary methods because they're not strictly required for mappings.

A shorter way to accomplish all of this is to inherit from UserDict:

    from collections import UserDict

    class PermaDict(UserDict):

        """Mapping that doesn't allow updating keys once set."""

        def __setitem__(self, key, value):
            if key in self:
                raise KeyError(f"{key} already in dictionary.")
            super().__setitem__(key, value)

The UserDict class in the collections module is a dictionary-like class that stores its data in a "data" attribute, as we were doing manually. It's implemented in Python instead of C (unlike dict) and it practices object- oriented programming well so customizing `__setitem__` will also change the behavior of the update method as well.

That's the easiest solution to the base problem and it's the one I'd recommend.

# Bonus #1

Force the second bonus we needed to make a force_set method that allows keys to be forcibly overridden.

To do this you can't simply make a method like this:

        def force_set(self, key, value):
            self[key] = value

This doesn't work because this will call our `__setitem__` method which will raise an exception.

We could instead set the item in the dictionary that our class wraps around:

Here's one way we could have done that:

        def force_set(self, key, value):
            self.data[key] = value

The UserDict class uses the "data" attribute to store a dictionary with our actual data in it.

If someone inherited from our class but used multiple inheritance with a mixin this may not delegate work to it though (depending on how the mixin was used).

So this may be a better idea:

        def force_set(self, key, value):
            super().__setitem__(key, value)

This delegates the item setting to our parent (or the next class up our method resolution chain). This works because our class is the one that modified `__setitem__` but our parent's `__setitem__` hasn't been modified. So we're able to skip our `__setitem__` method and go right to our parent's.

# Bonus #2

For the second bonus we were supposed to accept a "silent" argument to our class that, if True, would make our class silently ignore attempted updates to keys.

We definitely need to accept a silent argument to our initializer.

The problem is that our silent argument shouldn't be the first one, so this won't work:

        def __init__(self, silent=False, *args, **kwargs):
            self.silent = silent
            super().__init__(*args, **kwargs)

This will work though:

        def __init__(self, iterable=None, silent=False, **kwargs):
            self.silent = silent
            super().__init__(iterable, **kwargs)

Here we're manually accepting an iterable argument, defaulting it to None (which UserDict uses as the default for its first argument also) and then also accepting a silent argument followed by all other keyword arguments. Then we're capturing the value of silent and passing everything else to our parent.

We'll then need to use the silent attribute in our `__setitem__` method to ensure we don't raise an exception if it's True:

        def __setitem__(self, key, value):
            if key not in self:
                return super().__setitem__(key, value)
            if self.silent is not True:
                raise KeyError(f"{key} already in dictionary.")

We're using "is not" here instead of != because True is a singleton and using identity checks for singletons is recommended over using equality.

However, we might want to actually get less specific with our check and rely simply on the truthiness of "silent":

        def __setitem__(self, key, value):
            if key not in self:
                return super().__setitem__(key, value)
            if not self.silent:
                raise KeyError(f"{key} already in dictionary.")

If silent were set to a non-boolean value this would still work. We might see that as problematic though. If that's the case we should probably do some type checking on the value passed in. I wouldn't usually recommend that though as it's a somewhat uncommon practice in Python.

Another way we could have implemented our `__init__` method before is to grab the "silent" argument from the keyword arguments provided only:

        def __init__(self, *args, **kwargs):
            self.silent = kwargs.pop('silent', False)
            super().__init__(*args, **kwargs)

It really only makes sense for silent to be called as a keyword argument, so this isn't a bad way to do things.

We're removing the silent keyword argument from kwargs before we pass it to our parent class because UserDict doesn't know how to handle silent. We're also defaulting silent to False here.

We're really looking for a keyword-only argument here and there's a better way to do that in Python 3:

        def __init__(self, *args, silent=False, **kwargs):
            self.silent = silent
            super().__init__(*args, **kwargs)

Any arguments after *args in a function definition are considered keyword-only arguments. So silent here is an optional keyword-only argument that defaults to False.

# Bonus #3

For the third bonus we were supposed to accept a "force" keyword argument to our update method to force update our dictionary.

Using what we just discussed about keyword-only arguments, we could do that like this:

        def update(self, *args, force=False, **kwargs):
            if force:
                return self.data.update(*args, **kwargs)
            else:
                return super().update(*args, **kwargs)

If force is True (truthy really), we're calling the update method on the underlying data attribute that our dictionary data is stored in. If not, we're calling our parent's update method.

If we wanted to make sure our force_set method was called instead of delegating entirely to the dictionary we're wrapping, we could re-implement update like this:

        def update(self, other={}, force=False, **kwargs):
            if not force:
                return super().update(other, **kwargs)
            if isinstance(other, dict):
                for key, value in other.items():
                    self.force_set(key, value)
            elif other is not None:
                for key, value in other:
                    self.force_set(key, value)
            for key, value in kwargs.items():
                self.force_set(key, value)

Here we're manually accepting a single "other" argument, in addition to our "force" argument and other keyword arguments.

If force is falsey, we delegate to our parent's update method.

We defaulted "other" to an empty dictionary instead of None because our parent's update method will be unhappy if we pass None to it.

If force is truthy, we do all the work we did when we originally re- implemented the update method, except we call force_set instead of setting keys using using the item setter syntax (since we want to force set these keys specifically).

Note that people sometimes talk about how you shouldn't use a [mutable default value](http://effbot.org/zone/default-values.htm) for your function arguments. This is only a concern if your function either mutates or returns the argument it's being passed. If it just loops over it (as in our case with that empty dictionary), there's not much reason not to use a mutable default value.

My preference is to use the shorter update method that delegates to our the dictionary we're wrapping. It doesn't call force_set, but if we really need that behavior, we can always re-implement this method the more verbose way later.

So this is the solution I most prefer:

    from collections import UserDict

    class PermaDict(UserDict):

        """Mapping that doesn't allow updating keys once set."""

        def __init__(self, *args, silent=False, **kwargs):
            self.silent = silent
            super().__init__(*args, **kwargs)

        def __setitem__(self, key, value):
            if key not in self:
                return super().__setitem__(key, value)
            if not self.silent:
                raise KeyError(f"{key} already in dictionary.")

        def force_set(self, key, value):
            return super().__setitem__(key, value)

        def update(self, *args, force=False, **kwargs):
            if force:
                return self.data.update(*args, **kwargs)
            else:
                return super().update(*args, **kwargs)

I hope you got some good practice with dictionaries this week!