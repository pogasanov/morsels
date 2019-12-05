import calendar
import datetime


class Weekday:
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def meetup_date(year, month, nth=4, weekday=Weekday.THURSDAY):
    DAYS_IN_WEEK = 7

    cal = calendar.Calendar(weekday)
    days = list(cal.itermonthdays(year, month))
    if nth < 0:
        counter = nth * DAYS_IN_WEEK
    else:
        counter = nth * DAYS_IN_WEEK if days[0] == 0 else (nth - 1) * DAYS_IN_WEEK
    return datetime.date(year=year, month=month, day=days[counter])
