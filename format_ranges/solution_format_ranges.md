# Solution: format_ranges

Hey!

If you haven't attempted to solve format_ranges yet, close this email and go do that now before reading on. If you have attempted solving format_ranges, read on...

This week you needed to make a function, `format_ranges` which accepted an iterable of numbers and returned a string with each of the consecutive ranges of numbers grouped together.

Here's one way to do this:

    def format_ranges(numbers):
        pairs = []
        start = end = None
        for n in numbers:
            if start is None:
                start = n
            elif n > end+1:
                pairs.append((start, end))
                start = n
            end = n
        pairs.append((start, end))
        return ",".join(
            f"{start}-{end}"
            for (start, end) in pairs
        )

We're building up a list of start and end pairs first. These are represented with tuples.

Then using a generator expression, a format string (Python 3.6+), and tuple unpacking to join our start and end values with `-` and to join each of those pairs with `,`.

Note that we're reusing the `start` and `end` variable names in our generator expression, but they're in they're own scope so our outer `start` and `end` variables won't actually be affected (not that we're using them after that `return` statement anyway).

Here's another similar way we could have solved this:

    def format_ranges(numbers):
        pairs = []
        last = None
        for n in numbers:
            if last is None:
                pairs.append([n])
            elif n > last+1:
                pairs[-1].append(last)
                pairs.append([n])
            last = n
        pairs[-1].append(n)
        return ",".join(
            f"{start}-{end}"
            for (start, end) in pairs
        )

Here we're using a list of lists instead of a list of tuples and we're mutating each of the inner tuples as we add our `end` values.

I find this a bit more cryptic than using tuples with `start` and `end` variables to temporarily store our current start and end values.

# Bonus #1

For the first bonus we needed our function to work well with single number ranges.

We could change our generator expression into a `for` loop with an `if` statement to handle this:

    def format_ranges(numbers):
        pairs = []
        start = end = None
        for n in numbers:
            if start is None:
                start = n
            elif n > end+1:
                pairs.append((start, end))
                start = n
            end = n
        pairs.append((start, end))
        pair_strings = []
        for (start, end) in pairs:
            if start == end:
                pair_strings.append(str(start))
            else:
                pair_strings.append(f"{start}-{end}")
        return ",".join(pair_strings)

You might notice that we could actually use an _inline if statement_ to collapse that if-else appending situation into a single line:

        for (start, end) in pairs:
            pair_strings.append(str(start) if start == end else f"{start}-{end}")

That would make this something we could [copy-paste into a list comprehension](https://treyhunner.com/2015/12/python-list-comprehensions-now-in-color/)... or back into a generator expression as we had before:

    def format_ranges(numbers):
        pairs = []
        start = end = None
        for n in numbers:
            if start is None:
                start = n
            elif n > end+1:
                pairs.append((start, end))
                start = n
            end = n
        pairs.append((start, end))
        return ",".join(
            f"{start}-{end}" if start != end else f"{start}"
            for (start, end) in pairs
        )

Note that I switched between `str(start)` and `f"{start}"`. I'm undecided on whether I like f-strings that just have a single variable and nothing else in them. The `str` constructor was designed just for this purpose, so there's not much point in making an f-string. I don't find one more or less readable than the other though.

# Bonus #2

For the second bonus we needed to allow our numbers to be unordered.

This one was somewhat trivial. We could just put this at the top of our function:

        numbers = sorted(numbers)

The `sorted` function will return a new list of sorted numbers, which we're then storing back into the same `numbers` variable.

You might be hesitant to reuse the same `numbers` variable here. If Python was _pass by reference_, this would trample on the original object that was passed into our function. But Python doesn't work that way. The original `numbers` list that was passed to us will be forgotten by our function. Presumably it's still referenced by some other variable and therefore floating around in memory, but we don't have access to it anymore. The new `numbers` variable points to a newly sorted list.

You may have tried this:

        numbers.sort()

This is a bad idea for a couple reasons:

1.  The original list object that was passed to us would be sorted in-place and the person who called our function might be upset that we sorted their list for them
2.  This won't work on iterables that don't have a `sort` method (like generators or iterators for example)

# Bonus #3

For the third bonus we needed to do something a bit more complicated: we needed to allow duplicate numbers. We weren't supposed to ignore duplicates, we were supposed to include duplicates in their own ranges.

One way to do this is through recursion. We could make a function that builds up the pairs we need and have that function call itself whenever it found duplicates.

    def format_ranges(numbers):
        pairs = make_ranges(sorted(numbers))
        return ",".join(
            f"{start}-{end}" if start != end else f"{start}"
            for (start, end) in pairs
        )

    def make_ranges(numbers):
        pairs = []
        start = end = None
        leftover = []
        for n in numbers:
            if start is None:
                start = n
            elif n > end+1:
                pairs.append((start, end))
                start = n
            elif n == end:
                leftover.append(n)
            end = n
        pairs.append((start, end))
        if leftover:
            pairs += make_ranges(leftover)
        return sorted(pairs)

So `format_ranges` now delegates the pair-making to a `make_ranges` function.

That `make_ranges` function does the same thing we were doing before to build up pairs, except when we encounter a number that was equal to the one before it, we throw it in the `leftover` list.

If our `leftover` list is non-empty after we're done looping, we call `make_ranges` on it and extend our own `pairs` list with the resulting pairs. Then we sort the results and return them.

If we have a number that occurs more than 2 times, our `make_ranges` function will recursively call itself more than once, as deep as it needs to.

Another way to do this is to keep track of both the unique numbers in order and the number of times we see each number and then take one of each number in order, looping back to the beginning over and over until we have no more numbers left.

    from collections import Counter

    def format_ranges(numbers):
        pairs = []
        counts = Counter(sorted(numbers))
        while counts:
            start = end = None
            for n in counts.keys():
                counts[n] -= 1
                if start is None:
                    start = n
                elif n > end+1:
                    pairs.append((start, end))
                    start = n
                end = n
            pairs.append((start, end))
            counts = +counts
        pairs.sort()
        return ",".join(
            f"{start}-{end}" if start != end else f"{start}"
            for (start, end) in pairs
        )

We're using `Counter` and `sorted` to keep track of the number of times we see each number in order. There are many ways to keep track of the counts of things in Python, but [Counter is often the best way to do this](https://treyhunner.com/2015/11/counting-things-in-python/). The **in order** part only works in Python 3.6 or higher because dictionaries are ordered in Python 3.6 and above.

Our `while counts` loop is doing everything inside it as long as `counts` is non-empty (meaning it has at least one key-value pair).

We're looping over the keys in our `counts` object, and decrementing each by one. Then we do just what we did in our first answer (keep track of whether we're still consecutive or whether we've reached the end of a pair).

That `counts = +counts` line is a little cryptic. That asks our `Counter` object to remove all key-value pairs from our `Counter` for which the value isn't positive. That's the magic that makes our `while counts` _not_ loop forever. We're removing values once they reach a count of `0`.

After this, our `pairs` list is all out of order. If we sort it, we'll end up sorting by `start` first and `end` second for each pair (which happens to be exactly what we're looking for).

I like the `Counter` solution because it's interesting, but I think the recursive solution might be a little more clear. It's a little counter-intuitive (no pun intended) that our `Counter` is keeping track of the order of these numbers and that `counts = +counts` removes numbers that have hit a count of zero.

I hope you had fun with this week's exercise.