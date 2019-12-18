# Solution: FuzzyString

Hey!

If you haven't attempted to solve FuzzyString yet, close this email and go do that now before reading on. If you have attempted solving FuzzyString, read on...

This week you needed to make a class which acts like a string (in its two ways of being converted to a string) and compares as equal to similar strings in a case insensitive way.

Here's a way we could implement this manually:

    class FuzzyString:
        def __init__(self, string):
            self.string = string
        def __eq__(self, other):
            return self.string.lower() == other.lower()
        def __str__(self):
            return self.string
        def __repr__(self):
            return repr(self.string)

This is an object that works with the built-in `str` and `repr` functions and with the `==` and `!=` operators.

We could get some of this for free by inheriting from the `str` type:

    class FuzzyString(str):
        def __eq__(self, other):
            return self.lower() == other.lower()
        def __ne__(self, other):
            return self.lower() != other.lower()

Here we get our initializer and two string representations for free, but we need to implement `__ne__` ourselves because strings implement both `__eq__` and `__ne__` manually (normally `__ne__` is just the opposite of `__eq__` by default, but that's not the case on `str`).

A better way to create our own string type in a predictable way is to inherit from `collections.UserString`:

    from collections import UserString

    class FuzzyString(UserString):
        def __eq__(self, other):
            return self.data.lower() == other.lower()

The `UserString` class sets a `data` attribute in its initializer which stores the string we're wrapping around. We were practicing inheritance before, but we're practicing both inheritance and composition now because `UserString` is _wrapping around_ an actual string object, instead of inheriting from `str` itself.

# Bonus #1

For the first bonus we needed to allow the various ordering operators to work in a case-insensitive way.

If we just implemented our class without inheritance, we could have done that this way:

    from functools import total_ordering

    @total_ordering
    class FuzzyString:
        def __init__(self, string):
            self.string = string
        def __lt__(self, other):
            return self.string.lower() < other.lower()
        def __eq__(self, other):
            return self.string.lower() == other.lower()
        def __str__(self):
            return self.string
        def __repr__(self):
            return repr(self.string)

Here we're implementing just `__eq__` and `__lt__`. That `total_ordering` class decorator sees those methods and implements `__le__`, `__ge__`, and `__gt__` for us automatically.

If we wanted to do this same thing while inheriting from `UserString` we'd have to do something awkward:

    from collections import UserString
    from functools import total_ordering

    @total_ordering
    class FuzzyOrderingMixin:
        def __lt__(self, other):
            return self.data.lower() < other.lower()
        def __eq__(self, other):
            return self.data.lower() == other.lower()

    class FuzzyString(FuzzyOrderingMixin, UserString):
        """String which compares in a case-insensitive way."""

We have to practice multiple inheritance using a "mixin" class to get `total_ordering` to work because the `UserString` class implements the other comparisons by default, so `total_ordering` will ignore them and won't actually do anything useful for us if we just decorated our `FuzzyString` class directly.

This feels a bit like a hack, but it works consistently.

We could of course just implement all of these methods manually like this:

    from collections import UserString

    class FuzzyString(UserString):
        def __lt__(self, other):
            return self.data.lower() < other.lower()
        def __gt__(self, other):
            return self.data.lower() > other.lower()
        def __le__(self, other):
            return self.data.lower() <= other.lower()
        def __ge__(self, other):
            return self.data.lower() >= other.lower()
        def __eq__(self, other):
            return self.data.lower() == other.lower()

This is very repetitive, but a bit simpler for new Python programmers to understand.

# Bonus #2

For the second bonus, we needed to allow case insensitive containment checks (with the `in` operator) and case insensitive concatenation (concatenating should return a new `FuzzyString`.

Without inheritance, we could do this:

    from functools import total_ordering

    @total_ordering
    class FuzzyString:
        def __init__(self, string):
            self.string = string
        def __lt__(self, other):
            return self.string.lower() < other.lower()
        def __eq__(self, other):
            return self.string.lower() == other.lower()
        def __str__(self):
            return self.string
        def __repr__(self):
            return repr(self.string)
        def __add__(self, other):
            return FuzzyString(self.string + other)
        def __contains__(self, substring):
            return substring.lower() in self.string.lower()

We needed to implement concatenation ourselves here with `__add__`, but if we use `UserString` we'll get that for free:

    from abc import ABC, abstractmethod
    from functools import total_ordering
    from collections import UserString

    @total_ordering
    class Ordered(ABC):
        """Mixin class which defines <=, >, >= based on < and ==."""
        @abstractmethod
        def __lt__(self, other):
            """Child class must implement __lt__."""
        @abstractmethod
        def __eq__(self, other):
            """Child class must implement __eq__."""

    class FuzzyString(Ordered, UserString):
        def __lt__(self, other):
            return self.data.lower() < other.lower()
        def __eq__(self, other):
            return self.data.lower() == other.lower()
        def __contains__(self, substring):
            return substring.lower() in self.data.lower()

Note that we're doing something a bit different with our class mixin here. We're defining `__lt__` and `__eq__` in our `FuzzyString` class but all 6 comparison operators work because we're inheriting from a generic `Ordered` class that we've written to make it easier to use `total_ordering` in an inheritance situation.

This `Ordered` class can be used in any similar situation. If you've never made an "abstract" class using `abc.ABC` before, you may want to look into it. It's not something I've found a use for often, but the ability to define a _interface_ or _abstract class_ can be a useful tool to have in your toolbox.

# Bonus #3

For the third bonus, we needed to make our comparisons work for the same characters written in different ways in unicode.

There are two things we need to do to accomplish this. The first is to make sure we're normalizing case in a unicode-aware way. We can do this by using the string `casefold` method instead of the `lower` method:

    class FuzzyString(Ordered, UserString):
        def __lt__(self, other):
            return self.data.casefold() < other.casefold()
        def __eq__(self, other):
            return self.data.casefold() == other.casefold()
        def __contains__(self, substring):
            return substring.casefold() in self.data.casefold()

We really should have been using `casefold` all along. Whenever you want to normalize case in a string, the `casefold` method is the preferable way to do it. This lowercases our string in a way that takes into account things like `ß` and `ss` being equivalent (in German).

This doesn't pass our tests though. Our tests require that characters that are equivalent but composed in different ways are seen as equal. We can accomplish this by normalizing our text, using a decomoposed form like this:

    from abc import ABC, abstractmethod
    from functools import total_ordering
    from collections import UserString
    import unicodedata

    def normalize(string):
        return unicodedata.normalize("NFD", string.casefold())

    @total_ordering
    class Ordered(ABC):
        """Mixin class which defines <=, >, >= based on < and ==."""
        @abstractmethod
        def __lt__(self, other):
            """Child class must implement __lt__."""
        @abstractmethod
        def __eq__(self, other):
            """Child class must implement __eq__."""

    class FuzzyString(Ordered, UserString):
        def __lt__(self, other):
            return normalize(self.data) < normalize(other)
        def __eq__(self, other):
            return normalize(self.data) == normalize(other)
        def __contains__(self, substring):
            return normalize(substring) in normalize(self.data)

We've written a `normalize` function to reduce code repetition.

If you ever need to do comparisons on unicode data, you'll want to look up unicode text normalization.

I hope you learned something new this week about strings, abstract classes, or comparisons in Python!