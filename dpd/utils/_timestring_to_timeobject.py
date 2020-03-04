import datetime


def timestring_to_timeobject(timestring):
    """
    handle the case where hours go past midnight
    """
    days = 0
    hours = int(timestring[0:2])
    while hours > 23:
        days += 1
        hours -= 24
    timestring = str(hours) + timestring[2:]
    return datetime.datetime.strptime(timestring, "%H:%M:%S") + datetime.timedelta(
        days=days
    )
