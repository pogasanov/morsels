# Solution: meetup_date

Hiya!

If you haven't attempted to solve meetup_date yet, close this email and go do that now before reading on. If you have attempted solving meetup_date, read on...

This week you were supposed to write a function that determined a meetup date for a given year and month.

At first your function was supposed to always return the 4th Thursday of the month.

Here's one solution:

    from datetime import date, timedelta

    THURSDAY = 3

    def meetup_date(year, month):
        """Return date of the fourth Thursday of the given month."""
        first_day_of_the_month = date(year, month, 1)
        shift = timedelta((THURSDAY - first_day_of_the_month.weekday()) % 7)
        first_thursday = first_day_of_the_month + shift
        return first_thursday + timedelta(weeks=3)

Here we're getting the first date of the month and then using it to figure out what the first thursday of the month is. Python's date objects have a weekday method that returns an integer representing the weekday, from 0 (Monday) to 6 (Sunday).

We're taking 3 (Thursday) and subtracting the weekday of the first day of the month from it to get the number of days we need to shift by. We're then dividing that by 7 and taking the remainder (that's what % 7 does) and creating a timedelta object from that. Python's timedelta objects represent a duration of time.

Once we've shifted the first day of the month to get the first Thursday, we can then add 3 weeks to get the fourth one.

There's another standard library module we could use to help us solve this problem. The calendar module:

    from datetime import date
    from calendar import monthcalendar, THURSDAY

    def meetup_date(year, month):
        """Return date of the fourth Thursday of the given month."""
        cal = monthcalendar(year, month)
        if cal[0][THURSDAY] == 0:
            nth_of_month = 4
        else:
            nth_of_month = 3
        day_of_fourth_thursday = cal[nth_of_month][THURSDAY]
        return date(year, month, day_of_fourth_thursday)

The calendar module has some odd but useful stuff in it. We're using monthcalendar here to get a list of lists representing a calendar.

It's like a mini calendar in list form:

    >>> from calendar import monthcalendar
    >>> for week in monthcalendar(2020, 1):
    ...     print(week)
    ...
    [0, 0, 1, 2, 3, 4, 5]
    [6, 7, 8, 9, 10, 11, 12]
    [13, 14, 15, 16, 17, 18, 19]
    [20, 21, 22, 23, 24, 25, 26]
    [27, 28, 29, 30, 31, 0, 0]

We're checking to see whether or not the first week in our month includes a Thursday (that Thursday will be 0 if it doesn't). If it does, then we'll grab the 4th row (index 3), otherwise we'll grab the 5th (index 4).

After we've grabbed the day of the month for that Thursday from our list of lists, we construct a date object representing it.

Note that we're also importing THURSDAY from the calendar module, which happens to be the number 3, just like our THURSDAY variable before.

There's another tool in the calendar module to help us with this though:

    from calendar import Calendar, weekday, THURSDAY

    def meetup_date(year, month):
        """Return a date of the fourth Thursday of the given month."""
        nth = (
            4
            if weekday(year, month, 1) != THURSDAY
            else 3
        )
        thursday_calendar = Calendar(THURSDAY).monthdatescalendar(year, month)
        return thursday_calendar[nth][0]

The Calendar class gives an object that represents a calendar with the first day of each week starting on the given weekday (Thursday in our case).

if the month does not start on a Thursday, we set "nth" to 4 and we set it to 3 if it does. We do this because if our month doesn't start on a Thursday, we'll end up with one week that doesn't include a Thursday first.

This solution is clever, but I find it a bit more cryptic than our other two solutions. It's unusual to start a calendar on a Thursday, so relying on that functionality doesn't clarify much for a casual reader of our code.

# Bonus #1

For the first bonus we were supposed to accept optional nth and weekday arguments.

Here's one way to do this:

    from datetime import date, timedelta

    THURSDAY = 3

    def meetup_date(year, month, *, nth=4, weekday=THURSDAY):
        """Return date of the nth weekday of the given month."""
        first_day_of_the_month = date(year, month, 1)
        shift = timedelta((weekday - first_day_of_the_month.weekday()) % 7)
        return first_day_of_the_month + shift + timedelta(weeks=nth-1)

Here we've taken our datetime-based solution and substituted THURSDAY with our weekday variable and timedelta(weeks=3) with timedelta(weeks=nth-1).

Note that we're accepting these arguments as keyword arguments only (using that *). This wasn't explicitly required by our tests, but our tests also don't assume that these arguments can be used positionally so this does work.

Adapting our calendar.monthcalendar approach, we could do this:

    from datetime import date
    from calendar import monthcalendar, THURSDAY

    def meetup_date(year, month, *, nth=4, weekday=THURSDAY):
        """Return date of the nth weekday of the given month."""
        cal = monthcalendar(year, month)
        if cal[0][weekday] != 0:
            nth -= 1
        return date(year, month, cal[nth][weekday])

I find this very readable. That cal[nth][weekday] clearly grabs the nth week in our calendar and then grabs the specific weekday we're looking for in that week.

Using the calendar.Calendar object, we could do this:

    import calendar

    def meetup_date(year, month, *, nth=4, weekday=calendar.THURSDAY):
        """Return date of the nth weekday of the given month."""
        if calendar.weekday(year, month, 1) == weekday:
            nth -= 1
        return calendar.Calendar(weekday).monthdatescalendar(year, month)[nth][0]

I find the calendar.monthcalendar solution most readable at a glance, but the datetime solution is the most obvious and it's the one I'd typically think to reach for.

# Bonus #2

For the second bonus, we were supposed to allow our "nth" argument to accept negative numbers and count backward from the end of the month.

We can do this with calendar.monthscalendar solution like this:

    from datetime import date
    from calendar import monthcalendar, THURSDAY

    def meetup_date(year, month, *, nth=4, weekday=THURSDAY):
        """Return date of the nth weekday of the given month."""
        cal = monthcalendar(year, month)
        if nth > 0 and cal[0][weekday] != 0 or nth < 0 and cal[-1][weekday] == 0:
            nth -= 1
        return date(year, month, cal[nth][weekday])

That conditional is pretty complex now. The reason is that when we have a negative nth value, there could be a 0 in the last position for our given weekday, which means we'd need to subtract one from nth.

The calendar.Calendar solution actually makes this a bit simpler:

    import calendar

    def meetup_date(year, month, *, nth=4, weekday=calendar.THURSDAY):
        """Return date of the nth weekday of the given month."""
        if nth > 0 and calendar.weekday(year, month, 1) == weekday:
            nth -= 1
        return calendar.Calendar(weekday).monthdatescalendar(year, month)[nth][0]

The only change we made from our last calendar.Calendar solution was to add "nth > 0" as a condition for checking whether we need to subtract 1 from nth.

Solving this with the datetime module is a bit more complicated than with these calendar-module utilities.

It'd be easiest at this point if we made a helper function that returns a list of all Thursdays (or whatever weekday is specified).

We can do that like this:

    import datetime

    def weekdays_in_month(year, month, weekday):
        """Return list of all 4/5 dates with given weekday and year/month."""
        date = datetime.date(year, month, 1)
        date += datetime.timedelta(days=(7 + weekday - date.weekday()) % 7)
        first_to_fifth = (
            date + datetime.timedelta(days=7)*i
            for i in range(6)
        )
        return [
            date
            for date in first_to_fifth
            if date.month == month
        ]

This function gets the first of the given weekdays in the month specified and then makes a list of that day and the same day in the three or four following weeks (depending on how many are in the month).

So calling weekdays_in_month(2018, 5, THURSDAY), with THURSDAY being 3, would give us the five Thursdays that were in May 2018.

We can now rewrite our meetup_date function like this:

    def meetup_date(year, month, *, nth=4, weekday=THURSDAY):
        """Return date of the nth weekday of the given month."""
        return weekdays_in_month(year, month, weekday)[nth-1 if nth > 0 else nth]

Here we're getting all the matching weekdays in our month and then grabbing the nth-1 or the nth depending on whether nth is greater than 0 (the first one is index 0).

If we'd like, we could use the same meetup_date function and rewrite our weekdays_in_month function to use calendar.Calendar:

    from calendar import Calendar

    def weekdays_in_month(year, month, weekday):
        """Return list of all 4/5 dates with given weekday and year/month."""
        return [
            dates[0]
            for dates in Calendar(weekday).monthdatescalendar(year, month)
            if dates[0].month == month
        ]

I actually find this solution pretty clear despite the fact that calendar.Calendar is a bit confusing. I think it's easy to guess from the docstring and the comprehension we've written what we're getting back here.

However, I like the calendar.monthcalendar solution even more. Here it is in full:

    from datetime import date
    from calendar import monthcalendar, THURSDAY

    def weekdays_in_month(year, month, weekday):
        """Return list of all 4/5 dates with given weekday and year/month."""
        return [
            date(year, month, week[weekday])
            for week in monthcalendar(year, month)
            if week[weekday] != 0
        ]

    def meetup_date(year, month, *, nth=4, weekday=THURSDAY):
        """Return date of the nth weekday of the given month."""
        return weekdays_in_month(year, month, weekday)[nth-1 if nth > 0 else nth]

I find the weekdays_in_month approach makes this exercise more descriptive and understandable at a glance.

# Bonus #3

For the third bonus, we needed to make a namespace to store references to our weekdays, so that we can use can refer to variable names instead of hard-coded numbers.

We could do that by creating a class to use as a namespace, like this:

    class Weekday:
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

Then we can update our meetup_date function to default weekday to Weekday.THURSDAY:

    def meetup_date(year, month, *, nth=4, weekday=Weekday.THURSDAY):
        # ...

Another approach we could take is to use IntEnum:

    Weekday = IntEnum('Weekday', 'MONDAY TUESDAY WEDNESDAY THURSDAY FRIDAY SATURDAY SUNDAY')

This doesn't quite work though because IntEnum starts counting at 1 by default.

We could do this instead:

    import calendar
    from enum import IntEnum
    from itertools import count

    WEEKDAY_NAMES = [d.upper() for d in calendar.day_name]
    Weekday = IntEnum('Weekday', zip(WEEKDAY_NAMES, count()))

Here we're relying on the calendar.day_name iterable to provide us with each weekday starting with Monday. We're uppercasing each of them and then using itertools.count and zip to create an iterable of two-item tuples with the first item being the uppercased name of the weekday and the second item being its index (starting from 0).

Note that this won't work if our locale isn't set to an English-based one because the names in calendar.day_name change based on the locale we set.

If we wanted to be more explicit, but continue using IntEnum, we could just inherit from it:

    from enum import IntEnum

    class Weekday(IntEnum):
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

One benefit of this is that the attributes of our class will have a nice string representation, while also being seen as equal to the integers they represent.

    >>> Weekday.THURSDAY
    <Weekday.THURSDAY: 3>
    >>> Weekday.THURSDAY == 3
    True

I hope you learned something new this week!