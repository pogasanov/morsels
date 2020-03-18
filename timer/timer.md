# Timer

Greetings!

This week I'd like you to write a context manager called `Timer` which will record how long a block of code takes to execute.

    >>> from time import sleep
    >>> with Timer() as timer:
    ...     sleep(1.5)
    ...
    >>> timer.elapsed
    1.504882783210324

**Bonus 1**

For the first bonus I'd like you to record the elapsed times of each usage of the context manager in a `runs` attribute.

    >>> timer = Timer()
    >>> with timer:
    ...     x = sum(range(2**24))
    ...
    >>> timer.elapsed
    0.2696345190051943
    >>> with timer:
    ...     x = sum(range(2**25))
    ...
    >>> timer.elapsed
    0.5121023440151475
    >>> timer.runs
    [0.2696345190051943, 0.5121023440151475]

**Bonus 2**

For the second bonus I'd like you to allow `Timer` to be used as a decorator too:

    >>> @Timer
    ... def sum_of_squares(numbers):
    ...     return sum(n**2 for n in numbers)
    ...
    >>> sum_of_squares(range(2**20))
    384306618446643200
    >>> sum_of_squares(range(2**21))
    3074455146595352576
    >>> sum_of_squares.runs
    [0.35114182299003005, 0.6639977040467784]

**Bonus 3**

For the third bonus I'd like you to maintain `min`, `max`, `mean`, and `median` properties that keep track of these values for all runs in a given timer:

    >>> sum_of_squares(range(2**19))
    48038258586419200
    >>> sum_of_squares(range(2**22))
    24595649968853745664
    >>> sum_of_squares.runs
    [0.35114182299003005, 0.6639977040467784, 0.19335223210509866, 1.3423286559991539]
    >>> sum_of_squares.mean
    0.6377051037852652
    >>> sum_of_squares.median
    0.5075697635184042
    >>> sum_of_squares.min
    0.19335223210509866
    >>> sum_of_squares.max
    1.3423286559991539

**Hints**

*   [Writing a context manager](https://twitter.com/treyhunner/status/1222971242434715649 "A very short example of making a context manager")
*   [Much more info on context managers](https://alysivji.github.io/managing-resources-with-context-managers-pythonic.html "A detailed article on Python's context manager protocol")
*   [Recording elapsed time](https://pymotw.com/3/time/#performance-counter "time.perf_counter is a high resolution counter to measure elapsed time")
*   [Bonus 1: resetting start/stop appropriately](https://stackoverflow.com/questions/39611520/init-vs-enter-in-context-managers "You'll want to set the start time in the __enter__ method, not the __init__ method")
*   [Bonus 2: Writing a class based solution](https://treyhunner.com/2019/04/is-it-a-class-or-a-function-its-a-callable/#Callable_objects "Class instances can be called like function if they implement __call__ method")
*   [Bonus 2: A decorator helper for maintaining the original function name](https://stackoverflow.com/questions/308999/what-does-functools-wraps-do "functools.wraps preserves the metadata of the function you're decorating")
*   [Bonus 3: Calculating `mean` and `median`](https://docs.python.org/3/library/statistics.html#module-statistics "Python's statistics module has mean and median functions")
*   [Bonus 3: Getting `min` and `max` value](https://treyhunner.com/2019/05/python-builtins-worth-learning/#min_and_max "Python builtin min and max return the minimum and maximum items in an iterable")
*   [Bonus 3: Making auto-updating attributes](https://www.youtube.com/watch?v=jCzT9XFZ5bw "Properties are the way we make auto-updating attributes on Python classes")

**Tests**

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/044b3b6f0c684c7daa096e18798c9497/tests/). You'll need to write your code in a module named timer.py next to the test file. To run the tests you'll run "python test_timer.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.