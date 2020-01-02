# Solution: is_perfect_square

Hey! 🙂

If you haven't attempted to solve is_perfect_square yet, close this email and go do that now before reading on. If you have attempted solving is_perfect_square, read on...

This week's exercise required you to make a function that returns True when given a number which is the square of an integer. This might have seemed like an easier problem, but there's a number of ways to solve it.

Let's take a look at some solutions.

If you're new to Python, you might try something like this:

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        return int(number**0.5)**2 == number

You might notice that this answer doesn't pass one of the tests. If a Decimal number is passed to this function it will fail.

To fix that we can use the sqrt function from the math module:

    from math import sqrt

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        return int(sqrt(number))**2 == number

Another benefit of this solution is that sqrt(number) is more descriptive than number**0.5.

So this solution is taking the square root of the number, rounding it down (the int constructor truncates the float that comes back to make it into an int), squaring it, and comparing it to itself. If converting result of the square root to an integer doesn't change anything, that means the square root was an integer all along, which means the number is a perfect square.

Here's a variant of that solution:

    from math import sqrt

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        return sqrt(number) == int(sqrt(number))

Notice here we're comparing the square root to the square root converted to an integer. We could have also made a variable to store sqrt(number) if we decided we should avoid computing the square root twice.

Another solution you may have come up with involves the modulo operator:

    from math import sqrt

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        return sqrt(number) % 1 == 0

I find this one a little more confusing personally, but if you're familiar with the construct of "n % 1 == 0" being a check for integer-ness, then this might not be so unclear after all.

All of these solutions work, but there's one solution that I'd argue is certainly the most descriptive solution:

    from math import sqrt

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        return sqrt(number).is_integer()

If you read this code in English you'll see that we're checking whether the square root of the given number is an integer. That's pretty much the definition of a perfect square.

Coming up with that solution would have required you to look through the methods on floating point numbers and find the is_integer method and realize that sqrt() always gives us back a float return value so we can always call is_integer on it.

Alright let's talk about the bonuses...

# Bonus #1

First, how could we modify this function to return False for negative numbers? Well we could "look before we leap" and check if the number is negative before we take its square root:

    from math import sqrt

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        if number < 0:
            return False
        return sqrt(number).is_integer()

This does work and it's not bad code. You might also consider another way of doing this though. It's common in Python to practice a programming principle called "easier to ask forgiveness than permission". With this principle we would attempt to take the square root and handle an exception if that didn't work:

    from math import sqrt

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        try:
            return sqrt(number).is_integer()
        except ValueError:
            return False

This works the same way because taking the square root of a negative number raises a ValueError but passing strings, complex numbers, and other invalid types of data to the square root function raises a TypeError.

If attempting to check negative numbers was uncommon, this would be more efficient on average because it'd avoid that if-statement. If we expect it to be fairly common to check negative numbers with our function, we may want to use the if-statement because the exception handling overhead is non-existent when there is no exception but a little slower when there is one.

Okay now let's talk about the second bonus...

# Bonus #2

The second bonus was quite a bit more challenging. Integers in Python can be arbitrarily large. Python doesn't have integer overflow, so big numbers like 2**10000 are valid integers in Python.

This poses a bit of a problem for us. Taking the square root of any number will give us back a floating point numbers and floats have finite precision, unlike integers. So we'll lose precision when we take the square root of a very large integer, so when we ask if it's an integer the result may be True because of rounding errors.

If we want our function to work with arbitrarily large numbers, we need to allow for arbitrary precision when we take square roots. For this we'll need to switch to using the Decimal class from Python's built-in decimal module, instead of float.

Here's an attempt:

    from decimal import Decimal

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        return int(Decimal(number).sqrt())**2 == number

Notice that we're not writing sqrt(Decimal(number)) but Decimal(number).sqrt(). The reason for this is that the math.sqrt function returns a floating point number, but we want a Decimal number back. The sqrt method on Decimal objects computes the sqrt in a precise way.

This works for fairly large numbers now:

    >>> is_perfect_square(1586375448590241)
    True
    >>> is_perfect_square(1420958445736851)
    False

But it doesn't work for even larger numbers:

    >>> is_perfect_square(702885858507391689)
    True
    >>> is_perfect_square(702885858507391688)
    False

This is a little complex to fix. The issue here is that decimal.Decimal numbers have a finite precision just like floating point numbers do, but it can be changed. The default precision is 28\. We need the precision to increase based on the length of our integer though. To be on the safe side, let's set the precision to the number of digits in our number multiplied by 2\. We can do this like so:

    from decimal import Context, Decimal, localcontext

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        digit_count = len(str(number))
        with localcontext(Context(prec=digit_count*2)):
            return int(Decimal(number).sqrt())**2 == number

We're converting our number to a string and taking its length to get the number of digits. Then we're using a context manager called localcontext to temporarily set the precision for all Decimal objects to the digit count multiplied by 2\. Then we do exactly what we did before.

This is a little complex and it's likely not quite bug-free yet, but if we need something that works with big integers this will probably do what we're looking for.

Note that if we're really not worried about really big numbers being passed to our function, we really shouldn't go through all this hassle. If we wanted to, we could make an if statement that disallowed very large numbers or we could note in our docstring that very large numbers may return inaccurate answers.

If we want to make this answer complete, there is one more thing we should do though. You may notice that our function once again fails on negative numbers. it also fails on non-numeric types now because it no longer raises TypeError like it did before (now we get decimal.InvalidOperation). We could fix this by adding our if check back in, which should catch type errors for objects that can't be compared to numeric types:

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        if number < 0:
            return False
        digit_count = len(str(number))
        with localcontext(Context(prec=digit_count*2)):
            return int(Decimal(number).sqrt())**2 == number

This is a silly problem, but hopefully it helped you think about the way integers and floating point numbers work in Python.

For an even sillier problem, let's take a look at the third bonus.

# Bonus #3

For this bonus we were supposed to allow our function to check whether numbers are "complex perfect squares", meaning the complex square root of the given number has integers for both its imaginary and real parts.

The cmath library built-in to the standard library can be used for this. This library includes a complex square root function:

    import cmath

    def is_perfect_square(number, *, complex=False):
        """Return True if given number is the square of an integer."""
        if complex:
            root = cmath.sqrt(number)
            return root.real.is_integer() and root.imag.is_integer()
        if number < 0:
            return False
        digit_count = len(str(number))
        with localcontext(Context(prec=digit_count*2)):
            return int(Decimal(number).sqrt())**2 == number

Notice that we're using a single `*` in our function definition here to force "complex" to be a keyword only argument. This function cannot be called with two positional arguments. Our complex argument must be using its name.

Also note that both the real and imag components of the complex number we get back from cmath.sqrt are floating point numbers, so we can call the float is_integer() method on both.

At the end of the day my favorite solution is this one:

    from math import sqrt

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        return sqrt(number).is_integer()

Or maybe this one if you needed negative numbers to return False instead of raising an exception:

    from math import sqrt

    def is_perfect_square(number):
        """Return True if given number is the square of an integer."""
        try:
            return sqrt(number).is_integer()
        except ValueError:
            return False

I hope you learned something new while solving this exercise!