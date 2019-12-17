# tags_equal

Hey friend!

This week's exercise might seem a bit uninteresting at first because it involves working with an HTML-like syntax at a low level. The purpose this week _isn't_ to familiarize yourself with HTML, but to get some practice with string manipulation in Python.

This week I'd like you to write a function that accepts two strings containing opening HTML tags and returns True if they have the same attributes with the same values.

Some examples of basic tag comparisons I'd like you to handle:

    >>> tags_equal("<img src=cats.jpg width=200 height=400>", "<IMG SRC=Cats.JPG height=400 width=200>")
    True
    >>> tags_equal("<img src=dogs.jpg width=999 height=400>", "<img src=dogs.jpg width=200 height=400>")
    False
    >>> tags_equal("<p>", "<P>")
    True
    >>> tags_equal("<b>", "<p>")
    False

This might sound complex and it sort of is.

To make things a little easier:

1.  Assume attributes don't have double/single quotes around them and don't contain spaces (until you get bonus 3)
2.  Don't worry about repeated attribute names or value-less attributes. Assume there won't be repeats (until you get to bonus 1)
3.  Assume all attributes are key-value pairs (until you get to bonus 2)
4.  Assume attributes have no whitespace around them (key=value and never key = value)

But your function must:

1.  Ignore order of attributes: the same attribute names/values in different order should be equivalent
2.  Ignore case for both attribute names and values (yes even ignore case for attribute values)

I encourage you to try solving this exercise without using the standard library at first. Everything but the last bonus should be relatively do-able without importing any libraries.

If you get your tests to pass, consider doing some of these bonuses. Make sure you don't spend too much time trying to get the second or third bonus done though.

For the first bonus, I'd like you to handle duplicate attribute names by allowing the _first_ one to "win" (ignoring any before the last) ✔️:

    >>> tags_equal("<LABEL FOR=id_email for=id_username>", "<LABEL FOR=id_email>")
    True
    >>> tags_equal("<LABEL FOR=id_email for=id_username>", "<LABEL FOR=id_username>")
    False

For the second bonus, I'd like you to allow attributes without a value ✔️:

    >>> tags_equal("<OPTION NAME=California SELECTED>", "<option selected name=california>")
    True
    >>> tags_equal("<option name=california>", "<option name=california selected>")
    False

For the third bonus I'd like you to handle single/double quotes around attribute values and attribute values to have spaces in them ✔️:

    >>> tags_equal("<input value='hello there'>", '<input value="hello there">')
    True
    >>> tags_equal("<input value=hello>", "<input value='hello'>")
    True
    >>> tags_equal("<input value='hi friend'>", "<input value='hi there'>")
    False

That last bonus may be pretty tricky and I recommend you reach for the standard library if you attempt it.

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/24ce703aa77646cc881b0837d5be2391/tests/). You'll need to write your function in a module named tags_equal.py next to the test file. To run the tests you'll run "python test_tags_equal.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.