# record_calls
##### Assigned from Advanced Level on 10/07/2019

Hi!

This week I'd like you to write a decorator function that will record the number of times a function is called.

Your decorator function should be called record_calls and it'll work like this:

    @record_calls
    def greet(name):
        """Greet someone by their name."""
        print(f"Hello {name}")

That record_calls-decorated greet function will now have a call_count attribute that keeps track of the number of times it was called:

    >>> greet("Trey")
    Hello Trey
    >>> greet.call_count
    1
    >>> greet()
    Hello world
    >>> greet.call_count
    2

Decorator functions are functions which accept another function and return a new version of that function to replace it.

So this should be the same thing as what we typed above:

    greet = record_calls(greet)

If you haven't ever made a decorator function before, you'll want to look up how to make one.

If you've made a decorator function before, you might want to attempt one of the bonuses.

For the first bonus I'd like you to make sure your decorator function preserves the name and the docstring of the original function. ✔️

So if we ask for help on the function above:

    >>> help(greet)

We should see something like this:

    Help on function greet in module __main__:

    greet(name)
        Greet someone by their name.

For the second bonus I'd like you to keep track of a "calls" attribute on our function that records the arguments and keyword arguments provided for each call to our function. ✔️

    >>> greet("Trey")
    Hello Trey
    >>> greet.calls[0].args
    ('Trey',)
    >>> greet.calls[0].kwargs
    {}
    >>> greet(name="Trey")
    Hello Trey
    >>> greet.calls[1].args
    ()
    >>> greet.calls[1].kwargs
    {'name': 'Trey'}

For the third bonus, add a return_value and an exception attribute to each of the objects in our calls list. If the function returned successfully, return_value will contain the return value. Otherwise, exception will contain the exception raised. ✔️

    >>> @record_calls
    ... def cube(n):
    ...     return n**3
    ...
    >>> cube(3)
    27
    >>> cube.calls
    [Call(args=(3,), kwargs={}, return_value=27, exception=None)]
    >>> cube(None)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "<stdin>", line 9, in wrapper
      File "<stdin>", line 3, in cube
    TypeError: unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'
    >>> cube.calls[-1].exception
    TypeError("unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'")

Automated tests for this week's exercise [can be found here](https://www.pythonmorsels.com/exercises/3ee85ad3481f428d99458b102cbda7c6/tests/). You'll need to write your function in a module named record_calls.py next to the test file. To run the tests you'll run "python test_record_calls.py" and check the output for "OK". You'll see that there are some "expected failures" (or "unexpected successes" maybe). If you'd like to do the bonus, you'll want to comment out the noted lines of code in the tests file to test them properly.