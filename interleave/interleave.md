# interleave
##### Assigned from Advanced Level on 12/16/2019

Hello!

For this week's problem, I want you to write a function called `interleave` which accepts two iterables of any type and return a new iterable with each of the given items "interleaved" (item 0 from iterable 1, then item 0 from iterable 2, then item 1 from iterable 1, and so on).

We are making an assumption here that both iterables contain the same number of elements.

Here's an example:

    >>> numbers = [1, 2, 3, 4]
    >>> interleave(numbers, range(5, 9))
    [1, 5, 2, 6, 3, 7, 4, 8]
    >>> interleave(numbers, (n**2 for n in nums))
    [1, 1, 2, 4, 3, 9, 4, 16]

For the first bonus, your `interleave` function should return [an iterator](https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/) ✔️:

    >>> i = interleave([1, 2, 3, 4], [5, 6, 7, 8])
    >>> next(i)
    1
    >>> list(i)
    [5, 2, 6, 3, 7, 4, 8]

For second bonus your `interleave` function should accept any number of arguments ✔️:

    >>> interleave([1, 2, 3], [4, 5, 6], [7, 8, 9])
    [1, 4, 7, 2, 5, 8, 3, 6, 9]

For the third bonus, your `interleave` function should work with iterables of different lengths. Short iterables should be skipped over once exhausted ✔️:

    >>> interleave([1, 2, 3], [4, 5, 6, 7, 8])
    [1, 4, 2, 5, 3, 6, 7, 8]
    >>> interleave([1, 2, 3], [4, 5], [6, 7, 8, 9])
    [1, 4, 6, 2, 5, 7, 3, 8, 9]

If you **get stuck** this week, give these hints a try:

*   [Looping over multiple things at once](https://treyhunner.com/2016/04/how-to-loop-with-indexes-in-python/ "use the built-in zip function")
*   [Creating an iterator](https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/ "use a generator function")
*   [Any number of arguments](https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/ "using asterisks to accept unlimited arguments")
*   [Hint for bonus 3](https://docs.python.org/3.6/library/functions.html#zip "implementation of the built-in zip function")

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/db5f9e6add674a26aa384c6fe302400c/tests/). You'll need to write your code in a module named interleave.py next to the test file. To run the tests you'll run "python test_interleave.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.