import datetime


def httpCompatible(date: datetime.datetime = datetime.datetime.now()):
    "Returns something like 'Sat, 10 Apr 2021 23:59:59 GMT', which can be put inside a HTTP response"
    return date.strftime('%a %d %b %H:%M:%S %Z').replace("%Z", "GMT")

def tomorrowThisTime():
    return datetime.datetime.now() + datetime.timedelta(hours=24)