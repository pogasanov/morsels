# deep_flatten
##### Assigned from Advanced Level on 10/21/2019

Hey there,

This week we're going to work on flattening iterables. I'd like to you write a function deep_flatten that accepts a list of lists (or lists of tuples and lists) and returns a flattened version of that list of lists.

It should work like this:

    >>> deep_flatten([[(1, 2), (3, 4)], [(5, 6), (7, 8)]])
    [1, 2, 3, 4, 5, 6, 7, 8]
    >>> deep_flatten([[1, [2, 3]], 4, 5])
    [1, 2, 3, 4, 5]

In the examples above, we're returning a list. Your deep_flatten function should return an iterable, not necessarily a list.

Your deep_flatten function can assume that no strings will be passed to it. We'll deal with strings later.

For the first bonus, I'd like you to make sure your deep_flatten function accepts not just lists and tuples, but generators, sets, and other iterable data structures (but don't worry about strings yet). ✔️

    >>> sorted(deep_flatten({(1, 2), (3, 4), (5, 6), (7, 8)})
    [1, 2, 3, 4, 5, 6, 7, 8]

For the second bonus, I'd like you to make deep_flatten return an iterator ✔️:

    >>> flattened = deep_flatten([[(1, 2), (3, 4)], [(5, 6), (7, 8)]])
    >>> next(flattened)
    1

For the third bonus, I'd like you to make sure deep_flatten works with strings ✔️:

    >>> list(deep_flatten([['apple', 'pickle'], ['pear', 'avocado']]))
    ['apple', 'pickle', 'pear', 'avocado']

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/05fe60de17824ef3ae77d93a3be2e98b/tests/). You'll need to write your function in a module named deep_flatten.py next to the test file. To run the tests you'll run "python test_deep_flatten.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.