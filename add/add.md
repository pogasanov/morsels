# add

Hey! ✨

I'd like you to write a function that accepts two lists-of-lists of numbers and returns one list-of-lists with each of the corresponding numbers in the two given lists-of-lists added together.

It should work something like this:

    >>> matrix1 = [[1, -2], [-3, 4]]
    >>> matrix2 = [[2, -1], [0, -1]]
    >>> add(matrix1, matrix2)
    [[3, -3], [-3, 3]]
    >>> matrix1 = [[1, -2, 3], [-4, 5, -6], [7, -8, 9]]
    >>> matrix2 = [[1, 1, 0], [1, -2, 3], [-2, 2, -2]]
    >>> add(matrix1, matrix2)
    [[2, -1, 3], [-3, 3, -3], [5, -6, 7]]

Try to solve this exercise without using any third-party libraries (without using pandas for example).

Before attempting any bonuses, I'd like you to put some effort into figuring out the clearest and most idiomatic way to solve this problem.

There are two bonuses this week.

**Bonus 1**

For the first bonus, modify your add function to accept and "add" any number of lists-of-lists. ✔️

    >>> add([[1, 9], [7, 3]], [[5, -4], [3, 3]], [[2, 3], [-3, 1]])
    [[8, 8], [7, 7]]

**Bonus 2**

For the second bonus, make sure your add function raises a ValueError if the given lists-of-lists aren't all the same shape. ✔️

    >>> add([[1, 9], [7, 3]], [[1, 2], [3]])
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "add.py", line 10, in add
        raise ValueError("Given matrices are not the same size.")
    ValueError: Given matrices are not the same size.

**Hints**

Hints for **when you get stuck** (hover over links to see what they're about):

*   [Iterating lists with indexes (and without)](http://treyhunner.com/2016/04/how-to-loop-with-indexes-in-python/ "When looping over multiple lists at once, indexes aren't usually necessary")
*   [Multiple assignment might come in handy](https://treyhunner.com/2018/03/tuple-unpacking-improves-python-code-readability/ "Multiple assignment is very common to see while looping")
*   [A special syntax for creating new lists from old lists](https://treyhunner.com/2015/12/python-list-comprehensions-now-in-color/ "List comprehensions are a special purpose tool for a special kind of looping")
*   [Accepting any number of arguments to a function](https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/#Asterisks_for_packing_arguments_given_to_function "*args and **kwargs idiom allows accepting multiple arguments passed to a function")
*   [More discussion on accepting any number of arguments](https://stackoverflow.com/questions/36901/what-does-double-star-asterisk-and-star-asterisk-do-for-parameters/36908#36908 "Lots of examples of * and ** in here")
*   [Raising an exception in Python](https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python "Examples of how to raise an manually exception in Python")

**Tests**

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/cb8fbdd52cf14f8cb31df4f06343cccf/tests/). You'll need to write your function in a module named add.py next to the test file. To run the tests you'll run "python test_add.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.

You'll receive some answers and links to resources explaining ways to solve this exercise within a few days. Don't peek at the answers before attempting to solve this on your own.