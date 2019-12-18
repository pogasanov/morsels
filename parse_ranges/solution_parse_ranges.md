Hey!

If you haven't attempted to solve parse_ranges yet, close this email and go do that now before reading on. If you have attempted solving parse_ranges, read on...

This week you were supposed to write a function, parse_ranges, that accepted a string representing ranges of numbers and returned an iterable of those numbers.

The string is comma-delimited and the numbers have a "-" between them.

Here's one way we might have solved this:

    def parse_ranges(ranges_string):
        """Return iterable based on string of number ranges."""
        numbers = []
        for group in ranges_string.split(','):
            values = group.split('-')
            start = int(values[0])
            stop = int(values[1])
            i = start
            while i <= stop:
                numbers.append(i)
                i += 1
        return numbers

We're splitting on comma first and then looping over the resulting number groups. We split each of those groups on a hyphen and take the two values that come back and convert them to integers to get the start and stop of a sub-range. Then we manually loop from start to stop, appending each item to a new list of numbers.

You might notice that we're not handling spaces around our numbers here... but our code still passes the tests.

We don't need to handle spaces because the int built-in does that for us. int(' 4') and int('4 ') are both the integer 4.

There's a couple ways we could start to improve this code.

Here's another way to do this:

    def parse_ranges(ranges_string):
      """Return iterable based on string of number ranges."""
        numbers = []
        for group in ranges_string.split(','):
            start, stop = group.split('-')
            for num in range(int(start), int(stop)+1):
                numbers.append(num)
        return numbers

We're using a Python range object to handle retrieving all the numbers we need to append here.

We're also using [multiple assignment](https://treyhunner.com/2018/03/tuple-unpacking-improves-python-code-readability/) to improve the readability and correctness of our code.

You might be wondering if we could use a list comprehension instead of loops here. We are building up a new list, but we've got that group splitting line there which complicates things.

So we need to figure out how to get our code into a format that involves only looping and appending. We could split our looping into two stages like this:

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = []
        for group in ranges_string.split(','):
            pairs.append(group.split('-'))
        numbers = []
        for start, stop in pairs:
            for num in range(int(start), int(stop)+1):
                numbers.append(num)
        return numbers

Here we have two sets of loops, one that builds up a "pairs" list and another that loops over that "pairs" list and builds up a "numbers" list.

We could [copy-paste this into list comprehensions](https://treyhunner.com/2018/03/tuple-unpacking-improves-python-code-
readability/) like this:

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = [
            group.split('-')
            for group in ranges_string.split(',')
        ]
        numbers = [
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        ]
        return numbers

Note that we're making a list here just to loop over it once. Whenever you're using a list comprehension to create a list that will only be looped over once, you could make a generator expression instead.

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = (
            group.split('-')
            for group in ranges_string.split(',')
        )
        return [
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        ]

Here we've made pairs into a generator expression and we've removed the unnecessary "numbers" variable and simply returned our resulting list immediately.

You might have thought to take a fairly different approach to this problem. We're parsing strings, which is something regular expressions are sometimes handy for.

    import re

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = re.findall(r'\b(\d+)-(\d+)\b', ranges_string)
        return [
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        ]

Those \b are word breaks. Note that we don't have commas anywhere in our regular expression. We're not splitting on commas, but instead finding all sets of consecutive digits separate by a hyphen which are at the ends of "words" (meaning they're at the beginning/end of the string or they have a comma, space, or other non-word character before/after them).

We could actually leave off those word boundaries as well if we didn't care whether our regular expression was even more lenient with the data provided to us.

Here's another way to use a regular expression:

    import re

    PAIRS_RE = re.compile(r'( \d+ ) - ( \d+ )', re.VERBOSE)

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        return [
            num
            for start, stop in PAIRS_RE.findall(ranges_string)
            for num in range(int(start), int(stop)+1)
        ]

Here we're pre-compiling the regular expression and then using it in our comprehension by referencing the object we stored the compiled regular expression in.

We also have VERBOSE mode enabled here to allow us to space out our regular expression for readability.

# Bonus #1

Let's try to tackle the first bonus.

For the first bonus we were supposed to return an iterator from our function.

We're currently returning a list by using a list comprehension. We could turn that list comprehension into a generator expression to return a generator instead:

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = (
            group.split('-')
            for group in ranges_string.split(',')
        )
        return (
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        )

Or we could go back to using a "for" loop and turn our function into a generator function that yields values.

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = (
            group.split('-')
            for group in ranges_string.split(',')
        )
        for start, stop in pairs:
            for num in range(int(start), int(stop)+1):
                yield num

One more improvement to this solution: we can use "yield from" instead of just "yield":

    def parse_ranges(ranges_string):
        pairs = (
            group.split('-')
            for group in ranges_string.split(',')
        )
        for start, stop in pairs:
            yield from range(int(start), int(stop)+1)

Whenever you see "for x in iterable: yield x" you can instead write "yield from iterable".

# Bonus #2

Let's try the second bonus now.

For the second bonus we needed to accept individual numbers in addition to start and end numbers for our ranges. So "1-4,6,8-9" should be valid and should represent [1, 2, 3, 4, 6, 8, 9].

We can do this by conditionally splitting on "-" only if "-" is present and doubling up our number otherwise:

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = (
            group.split('-') if '-' in group else (group, group)
            for group in ranges_string.split(',')
        )
        return (
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        )

Note that we're using an "inline if statement" here.

Whenever you see something like this:

    if something:
        x = thing1
    else:
        x = thing2

You could instead write this:

    x = thing1 if something else thing2

This "inline if statement" is similar to the [?: ternary operators](https://en.wikipedia.org/wiki/%3F:) in most other programming languages.

Another way we could do this is to not use an "inline if statement" and multiple assignment but instead rely on indexes:

    def parse_ranges(ranges_string):
        items = (
            group.split('-')
            for group in ranges_string.split(',')
        )
        return (
            num
            for item in items
            for num in range(int(item[0]), int(item[-1])+1)
        )

The split method returns a list of either 1 or 2 items and item[0] will always be the first and item[-1] will be the last (which will be the first if there's just 1 and will be the second if there's 2) so we don't need to check whether "-" is in our group at all.

I'm not a big fan of this solution because I find it a little unintuitive at first glance. I think removing the multiple assignment and "inline if" actually makes this code less readable in this case.

Another way we could do this is to use the string partition method instead of the split method:

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        partitions = (
            group.partition('-')
            for group in ranges_string.split(',')
        )
        pairs = (
            ((a, b) if b else (a, a))
            for (a, _, b) in partitions
        )
        return (
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        )

The partition method on strings partitions the string by splitting on the given separator ('-' in this case) and returns back the part before the partition (the head), the separator itself, and the part after the partition (the tail).

However partition works differently if there's no separator found. If no separator is found, an empty string is returned for the partition and the tail.

    >>> 'a-b'.partition('-')
    ('a', '-', 'b')
    >>> 'a'.partition('-')
    ('a', '', '')

So in our inline if statement above ("(a, b) if b else (a, a)") we're checking above whether there is a second value and if there isn't then we double up the first value in a new tuple.

That `(a, _, b)` is assigning the separator to the `_` variable. Assigning to an `_` variable is a common convention to use when you don't care about the value you're assigning to at all and you're just assigning to it during the process of unpacking other values.

Ned Batchelder actually wrote a blog post on solving this problem using a "Python gargoyle", which is what he's calling code that is surprising and something he wouldn't want to keep but interesting nonetheless:

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = (
            ((a, b) if b else (a, a))
            for group in ranges_string.split(',')
            for (a, _, b) in [group.partition('-')]
        )
        return (
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        )

Ned actually takes this a step further by using an int(b or a)+1 construct:

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        return (
            num
            for group in ranges_string.split(',')
            for a, _, b in [group.partition('-')]
            for num in range(int(a), int(b or a)+1)
        )

I find that (a or b) construct confusing in Python and I try to avoid it, though it's a common convention in many other programming languages (in JavaScript for example).

The gargoyle though is in this odd line:

        for (a, _, b) in [group.partition('-')]

You can read Ned's blog post, [A Python gargoyle](https://nedbatchelder.com/blog/201802/a_python_gargoyle.html) explaining that code snippet if you'd like.

Personally if I were going to adopt the usage of this gargoyle, I'd take it further and do this:

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        return (
            num
            for group in ranges_string.split(',')
            for (a, _, b) in [group.partition('-')]
            for (start, stop) in [((a, b) if b else (a, a))]
            for num in range(int(start), int(stop)+1)
        )

But I think this is awfully unreadable and I definitely wouldn't recommend adopting that "assignment-via-for" construct that you see in those middle two "for" lines.

Again, if you don't explain Ned's gargoyle, don't worry. It's interesting but hopefully something you won't run into in real code.

One last reasonable way to solve this before we move to the last bonus:

    def partition(sep, group):
        """Return (start, end) tuple from given number group."""
        a, _, b = group.partition(sep)
        return ((a, b) if b else (a, a))

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = (
            partition('-', group)
            for group in ranges_string.split(',')
        )
        return (
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        )

Here we've created a helper function to handle the retrieval of our (start, stop) tuple from each of our sub-ranges (4-6, 8, etc.).

I like this approach personally because I like that we've split off a tricky but small processing step into its own function so our original function doesn't have to worry about that step.

# Bonus #3

Okay let's take a look at the last bonus.

For the last bonus we had to ignore "-> thing" bits in our numeric ranges.

Here's one approach:

    def partition(sep, group):
        a, _, b = group.partition(sep)
        return ((a, b) if b and not b.startswith('>') else (a, a))

    def parse_ranges(ranges_string):
        pairs = (
            partition('-', group)
            for group in ranges_string.split(',')
        )
        return (
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        )

This is a bit complex. The b.startswith('>') check is there to take care of the number->exit case.

Here's another slightly more readable approach:

    def parse_ranges(ranges):
        for group in ranges.split(','):
            start, sep, end = group.partition('-')
            if end.startswith('>') or not sep:
                yield int(start)
            else:
                yield from range(int(start), int(end)+1)

Here we're using a generator function again. We're checking whether we've split -> and if we have we yield a single number. If not, we yield from a range of numbers.

Using a regular expressions can make this problem a bit easier.

One approach is to take all instances of "-> thing" and replace them with an empty string. We can do that like this:

    import re

    def partition(sep, group):
      """Return (start, end) tuple from given number group."""
        group = re.sub(r'->.*', r'', group)
        a, _, b = group.partition(sep)
        return ((a, b) if b else (a, a))

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = (
            partition('-', group)
            for group in ranges_string.split(',')
        )
        return (
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        )

We've refactored our partition function here to look for the regular expression ->. _in each group (._ represents any number of characters) and replace it with an empty string. We're using re.sub for this substitution.

Another approach we could take is to use re.search to search in our group for any number of digits, optionally followed by a dash and more consecutive digits. We're capturing the two groups of consecutive digits here using those parenthesis. That ?: thing is confusing (note that it has absolutely nothing to do with the ?: ternary operator I mentioned earlier). That's a non- capturing group ([more in the re docs](https://docs.python.org/3/library/re.html)).

Another way we could do this is to use findall to find our groups in the first place:

    import re

    PAIR_RE = re.compile(r'( \d+ )(?: - (\d+) )?', re.VERBOSE)

    def parse_ranges(ranges_string):
        """Return iterable based on comma-separated numeric ranges."""
        pairs = (
            ((a, b) if b else (a, a))
            for a, b in PAIR_RE.findall(ranges_string)
        )
        return (
            num
            for start, stop in pairs
            for num in range(int(start), int(stop)+1)
        )

We're nearly back to the first couple regular expression solutions we had with findall here, except that this regular expression has a non-capturing group to allow the "-" and second number to be optional (to pass the second bonus).

I'm not a huge fan of regular expressions but I do like this solution.

We could rewrite that compiled regular expression like this if we wanted to document what was going on:

    PAIR_RE = re.compile(r'''
        (
            \d+     # At least one digit
        )
        (?:         # A group of
            -       # A single dash
            (\d+)   # At least one digit
        )?          # That last dash and number are optional
    ''', re.VERBOSE)

The [VERBOSE flag](https://docs.python.org/3/library/re.html#re.VERBOSE) is pretty great.

Did you learn anything while solving this week's problem?