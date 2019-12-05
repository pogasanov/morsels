# Vector
##### Assigned from Advanced Level on 12/02/2019

Hello!

This week I'd like you to make a 3-dimensional `Vector` class which that works with multiple assignment, supports equality and inequality operators.

    >>> v = Vector(1, 2, 3)
    >>> x, y, z = v
    >>> print(x, y, z)
    1 2 3
    >>> v == Vector(1, 2, 4)
    False
    >>> v == Vector(1, 2, 3)
    True

The `Vector` class also must use `__slots__` for efficient attribute lookups, meaning other attributes won't be able to be assigned to it and it won't have a `__dict__` like most classes we make do.

    >>> v.a = 4
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'Vector' object has no attribute 'a'
    >>> v.__dict__
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'Vector' object has no attribute '__dict__'

The tests also check to make sure your `Vector` class doesn't support odd behavior that it shouldn't have (like support for `<` and `>`).

I recommend solving the main problem before attempting the bonuses. If you finish quickly, try some of the bonuses.

**Bonus 1**

For the first bonus, I'd like you to make your `Vector` objects support addition and subtraction with other `Vector` objects:

    >>> Vector(1, 2, 3) + Vector(4, 5, 6) == Vector(5, 7, 9)
    True
    >>> Vector(5, 7, 9) - Vector(3, 1, 2) == Vector(2, 6, 7)
    True

Note that addition and subtraction shouldn't work in-place: they should return a new `Vector` object.

**Bonus 2**

For the second bonus, I'd like your vector to support multiplication and division by numbers (this should return a new scaled vector):

    >>> 3 * Vector(1, 2, 3) == Vector(3, 6, 9)
    True
    >>> Vector(1, 2, 3) * 2 == Vector(2, 4, 6)
    True
    >>> Vector(1, 2, 3) / 2 == Vector(0.5, 1, 1.5)
    True

**Bonus 3**

For the third bonus, I'd like you to make your `Vector` class immutable, meaning the coordinates (`x`, `y`, and `z`) cannot be changed after a new `Vector` has been defined:

    >>> v = Vector(1, 2, 3)
    >>> v.x = 4
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
        raise AttributeError("Vectors are immutable")
    AttributeError: Vectors are immutable

**Hints**

Hints for **when you get stuck** (hover over links to see what they're about):

*   [Using `__slots__`](https://blog.usejournal.com/a-quick-dive-into-pythons-slots-72cdc2d334e "Use __slots__ for faster attribute access, to save memory usage and prevent new attributes at runtime")
*   [Multiple assignment requires iterable class](https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/#Generators_can_help_when_making_iterables_too "To make an iterable class, you'll need a __iter__ method which returns an iterator")
*   [Comparing multiple items for equality](https://treyhunner.com/2019/03/python-deep-comparisons-and-code-readability/#Deep_equality "An example of using deep comparisons for implementing __eq__")
*   [On reducing class boilerplate code](https://www.youtube.com/watch?v=epKegvx_Jws "In this talk I discuss using dataclasses to reduce boilerplate code")
*   [Bonus 1: overriding the `+` operator](https://stackoverflow.com/questions/46407931/add-two-class-objects "The __add__ method is needed to implement addition")
*   [Bonus 2: overriding the `*` operator is more challenging](http://www.openbookproject.net/thinkcs/python/english2e/ch15.html#operator-overloading "You'll need both __mul__ and __rmul__")
*   [Bonus 2: on implementing division](https://stackoverflow.com/questions/44970692/dividing-a-number-by-instances-of-my-class-in-python/44971166 "You'll need a __truediv__ method for division")
*   [Bonus 2: things to know about operator overloading](https://jcalderone.livejournal.com/32837.html "It's a best practice to return NotImplemented when binary operators are used with unknown types")
*   [Bonus 3: making an immutable class](https://stackoverflow.com/a/4828492 "Method overriding technique to write immutable class")
*   [Bonus 3: making an immutable class with dataclasses](https://treyhunner.com/easier-classes/#/7/2 "frozen=True")

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/ced757b8a1bd400bb983aa8a2eb0e8fe/tests/). You'll need to write your function in a module named vector.py next to the test file. To run the tests you'll run "python test_vector.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.