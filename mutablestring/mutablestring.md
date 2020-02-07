# MutableString

Hey!

This week I'd like you to make a class called `MutableString` which will act like a string, except it will be mutable.

**Aside**: if you didn't know, strings in Python are immutable, meaning no matter how hard you might try to change them you can't. All string operations return a new string object instead of mutating the one you already have.

So `MutableString` should work like this:

    >>> greeting = MutableString("Hello world!")
    >>> greeting
    'Hello world!'
    >>> greeting[4] = "a"
    >>> greeting
    'Hella world!'

Concatenation, containment checks, and string methods should work on your `MutableString` objects:

    >>> greeting = MutableString("Hello world!")
    >>> greeting.endswith('!')
    True
    >>> greeting + MutableString('!')
    'Hella world!!'
    >>> (greeting + '?').lower()
    'hello world!?'
    >>> 'la' in greeting
    True
    >>> len(greeting)
    12

**Bonus 1**

For the first bonus, I'd like you to make sure that you can assign and delete slices of `MutableString` objects:

    >>> greeting = MutableString("Hello world!")
    >>> greeting[6:-1] = "there"
    >>> greeting
    'Hello there!'
    >>> del greeting[5:-1]
    >>> greeting
    'Hello!'
    >>> del greeting[-1]
    >>> greeting
    'Hello world'

**Bonus 2**

For the second bonus, you should make sure various operations on your class return `MutableString` objects:

    >>> greeting = MutableString("Hello world!")
    >>> exclamation = greeting[-1]
    >>> hello = greeting[:5]
    >>> type(exclamation), type(hello)
    (<class 'MutableString'>, <class 'MutableString'>)
    >>> double_exclamation = exclamation + "!"
    >>> lowercased_hello = hello.lower()
    >>> type(double_exclamation), type(lowercased_hello)
    (<class 'MutableString'>, <class 'MutableString'>)
    >>> characters = list(double_exclamation)
    >>> [type(c) for c in characters]
    [<class 'MutableString'>, <class 'MutableString'>]

**Bonus 3**

For the third bonus, you should make sure that methods typically found on mutable sequences (`append`, `insert`, and `pop`) work on your `MutableString` objects:

    >>> greeting = MutableString("Hello world")
    >>> greeting.append("!")
    >>> greeting
    'Hello world!'
    >>> greeting.insert(5, "o")
    >>> greeting
    'Helloo world!'
    >>> greeting.pop(5)
    >>> greeting
    'Hello world!'
    >>> greeting.pop()
    'Hello world'

**Hints**

Hints for **when you get stuck** (hover over links to see what they're about):

*   [Inheriting from built-ins](https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/ "Inheriting from built-ins has downsides")
*   [Creating custom sequences](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes "MutableSequence can be used for making custom mutable sequences")
*   [Creating custom string-like classes](https://docs.python.org/3/library/collections.html#collections.UserString "The collections.UserString can be useful for creating custom strings")

**Tests**

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/a8d67d185e1c4aa2be8be8fe4fddf7d5/tests/). You'll need to write your code in a module named mutablestring.py next to the test file. To run the tests you'll run "python test_mutablestring.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.