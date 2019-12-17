# format_ranges

Hello!

This week I'd like you to write a function `format_ranges`, that takes a list of numbers and returns a string that groups ranges of consecutive numbers together:

    >>> format_ranges([1, 2, 3, 4, 5, 6, 7, 8])
    '1-8'
    >>> format_ranges([1, 2, 3, 5, 6, 7, 8, 10, 11])
    '1-3,5-8,10-11'

All runs of consecutive numbers will be collapsed into N-M ranges where N is the start of the consecutive range and M is the end.

This is sort of like the format that printers use for choosing which pages to print.

At first you can assume that all consecutive ranges of numbers will be at least 2 consecutive numbers long.

**Bonus 1**

For the first bonus, I'd like you to handle ranges of individual numbers specially: they should be represented as a single number, like this:

    >>> format_ranges([4])
    '4'
    >>> format_ranges([1, 3, 5, 6, 8])
    '1,3,5-6,8'

**Bonus 2**

For the second bonus, I'd like your function to work even if the given numbers are unordered:

    >>> format_ranges([9, 1, 7, 3, 2, 6, 8])
    '1-3,6-9'

**Bonus 3**

For the third bonus, I'd like you to handle duplicate numbers specially. Whenever a number occurs more than once, it should be considered as part of a separate range of numbers.

    >>> format_ranges([1, 9, 1, 7, 3, 8, 2, 4, 2, 4, 7])
    '1-2,1-4,4,7,7-9'
    >>> format_ranges([1, 3, 5, 6, 8])
    '1,3,5-6,8'

The ranges should always be ordered by the lowest start number and then shortest range (when the start numbers are the same).

**Hints**

Hints for **when you get stuck** (hover over links to see what they're about):

*   [Identifying groups of consecutive integers](https://stackoverflow.com/a/2154741/2633215 "A code snippet that identifies groups of consecutive integers")
*   [Converting a list of integers into a string](https://stackoverflow.com/a/28883101/2633215 "You can create a string making use of "str.join()" to concatenate strings from a list and using "str" as a separator between them.")
*   [A one-liner for checking a condition](https://stackoverflow.com/a/394814/2633215 "An inline-if might be handy when handling both a single and multiple number range")
*   [Counting the occurrences of numbers](https://stackoverflow.com/a/23241146/2633215 "collection.Counter can help keep track of duplicate numbers")

**Tests**

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/f3cd06185c964f5c859bc749c62a411a/tests/). You'll need to write your function in a module named format_ranges.py next to the test file. To run the tests you'll run "python test_format_ranges.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.