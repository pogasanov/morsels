# FancyReader

Hi,

This week I'd like you to make a custom CSV reader that acts slightly different from both `csv.reader` and `csv.DictReader`.

I'd like you to make a `FancyReader` callable that will accept an iterable of strings (which is what `csv.reader` accepts) and a `fieldnames` attribute representing the headers. This `FancyReader` callable will return an iterator that yields `Row` objects which represent each row.

    >>> lines = ['my,fake,file', 'has,two,rows']
    >>> reader = FancyReader(lines, fieldnames=['w1', 'w2', 'w3'])
    >>> for row in reader:
    ...     print(row.w1, row.w2, row.w3)
    ...
    my fake file
    has two rows

Your `FancyReader` should accept all the same arguments as `csv.reader`.

You don't need to worry about headers that are invalid variable names in Python: just **assume all headers are valid Python variable names**.

**Bonus 1**

For the first bonus, I'd like you to make sure your `Row` objects are iterable and have a nice string representation.

    >>> lines = ['my,fake,file', 'has,two,rows']
    >>> reader = FancyReader(lines, fieldnames=['w1', 'w2', 'w3'])
    >>> row = next(reader)
    >>> row
    Row(w1='my', w2='fake', w3='file')
    >>> w1, w2, w3 = row
    >>> w3
    'file'

**Bonus 2**

For the second bonus, I'd like you to make the `fieldnames` attribute optional. If no `fieldnames` attribute is specified, the first row should be automatically be read as a header row (and used in place of `fieldnames`).

    >>> lines = ['w1,w2,w3', 'my,fake,file', 'has,two,rows']
    >>> reader = FancyReader(lines)
    >>> for row in reader:
    ...     print(row.w1, row.w2, row.w3)
    ...
    my fake file
    has two rows

**Bonus 3**

For the third bonus, I'd like the return value of `FancyReader` to have a `line_num` attribute, the same way `csv.reader` does:

    >>> lines = 'red,1\nblue,2\ngreen,3'.splitlines()
    >>> reader = FancyReader(lines, fieldnames=['color', 'numbers'])
    >>> next(reader)
    Row(color='red', number=1)
    >>> reader.line_num
    2
    >>> next(reader)
    Row(color='red', number=1)
    >>> reader.line_num
    3

If you get stumped while working on the bonuses, you may want to take a look at the source code for `DictReader`. You could almost nearly copy what `DictReader` does if you wanted to. But if you want more of a challenge I recommend **not looking** at the `DictReader` source code (until you get stuck).

**Hints**

*   [Accepting any number of keyword arguments](https://treyhunner.com/2018/10/asterisks-in-python-what-they-are-and-how-to-use-them/#Asterisks_for_packing_arguments_given_to_function "This could help you pass all keyword arguments directly to csv.reader")
*   [Reading CSV data row-by-row](https://pymotw.com/3/csv/index.html "csv.reader returns data, row by row, from any iterable of lines")
*   [How to write an iterator](https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/ "Generator functions are the usual way we create functions that return iterators")
*   [Adding new attributes to an object dynamically](https://stackoverflow.com/a/45898499/2633215 "The built-in setattr can add any attribute to an object by its name")
*   [One more way to add attributes](https://stackoverflow.com/a/2466232/2633215 "Most classes store all their attributes in a \_\_dict\_\_ dictionary")
*   [Bonus 1: how to make a nice string representation on your Python objects](https://twitter.com/treyhunner/status/1215361099832418305 "You need to write a __repr__ method")
*   [Bonus 1: Creating your own iterable](https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/#Generators_can_help_when_making_iterables_too "In order to make an iterable, you'll need to make a __iter__ method")
*   [Bonus 1: making slightly nicer generator functions](https://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-new-yield-from-syntax-in-python-3 "yield from can yield each value from an iterable, one at a time")
*   [Bonus 1: avoiding writing a `Row` class](https://pymotw.com/3/collections/namedtuple.html "collections.namedtuple is a factory function for cretaing a lightweight tuple-like class")
*   [Bonus 2: Getting just the first row](https://treyhunner.com/2019/05/python-builtins-worth-learning/#next "You can pass a file or csv.reader object to the built-in next function to get the next row of data from it")
*   [Bonus 3: making an iterator class](https://treyhunner.com/2018/06/how-to-make-an-iterator-in-python/#Making_an_iterator:_the_object-oriented_way "You'll need both __iter__ and __next__ methods")

**Tests**

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/7271e894d9f24b8385ad6cda60c519e4/tests/). You'll need to write your function in a module named bettercsv.py next to the test file. To run the tests you'll run "python test_bettercsv.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.