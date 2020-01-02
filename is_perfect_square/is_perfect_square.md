# is_perfect_square

Hello! 👋

This week I want you to write a function that might seem simple at first, but there's a number of ways to solve it.

This week's function, `is_perfect_square`, accepts a number and returns `True` if it's a perfect square and `False` if it's not. A perfect square is any number which has an integer square root. So 25 is a perfect square but 24 is not, 9 is a perfect square but 8 is not, 100 is a perfect square but 1000 is not.

Here's an example:

    >>> is_perfect_square(64)
    True
    >>> is_perfect_square(65)
    False
    >>> is_perfect_square(100)
    True
    >>> is_perfect_square(1000)
    False

I also want you to make sure that this function raises a `TypeError` when an invalid type is given (integers and floats are fine but strings aren't) and I want you to make sure your function works with sensible alternative numeric types like [decimal.Decimal](https://docs.python.org/3/library/decimal.html).

There are a few bonuses this week. The second two are particularly tricky.

**Bonus 1**

The first bonus is to make sure your function returns False for negative numbers. ✔️

    >>> is_perfect_square(-1)
    False
    >>> is_perfect_square(-4)
    False

**Bonus 2**

The second bonus is to make sure your function works for really big numbers. ✔️

    >>> is_perfect_square(4624000000000000)
    True
    >>> is_perfect_square(4623999999999999)
    False

**Bonus 3**

The third bonus is to make your function accept an optional "complex" _keyword-only argument_ which will allow your function to check whether the given number is a perfect square in the complex number system. ✔️

    >>> is_perfect_square(-4, complex=True)
    True
    >>> is_perfect_square(-5, complex=False)
    False
    >>> is_perfect_square(512j, complex=True)
    True

To be a complex perfect square, the complex square root of the number must have integers for both its real part and its imaginary part.

Note that you don't need to handle really big complex numbers.

**Hints**

Hints for **when you get stuck** (hover over links to see what they're about):

*   [Solutions for the base problem](https://stackoverflow.com/q/44531084/98187 "There are a number of possible solutions to this")
*   [Bonus 2: square root of arbitrarily large numbers](https://stackoverflow.com/a/47854670/2633215 "You'll want to use decimal.Decimal to handle arbitrarily large decimal numbers precisely")
*   [Bonus 2: handling a large number of any size](https://pymotw.com/3/decimal/#local-context "localcontext can change the decimal precision temporarily")
*   [Bonus 3: complex numbers in Python](https://docs.python.org/3/library/cmath.html "The cmath module has a sqrt function too")
*   [Bonus 3: keyword-only arguments](https://treyhunner.com/2018/04/keyword-arguments-in-python/#Keyword-only_arguments_without_positional_arguments "An explanation of how to make keyword-only arguments when defining a function")

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/ad57c49f8a0042729e347cc34e8ac0e6/tests/). You'll need to write your function in a module named perfect_square.py next to the test file. To run the tests you'll run "python test_perfect_square.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.