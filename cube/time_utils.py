# -*- encoding: utf-8 -*-

"""
Copyright (c) 2013 Thomas Sileo
Copyright (c) 2012 Steven Buss
Originally from:
https://github.com/sbuss/pypercube/blob/master/pypercube/time_utils.py
"""

import re
from datetime import datetime, timedelta

STEP_10_SEC = long(1e4)
STEP_1_MIN = long(6e4)
STEP_5_MIN = long(3e5)
STEP_1_HOUR = long(36e5)
STEP_1_DAY = long(864e5)

STEP_CHOICES = ((STEP_10_SEC, "10 seconds"),
                (STEP_1_MIN, "1 minute"),
                (STEP_5_MIN, "5 minutes"),
                (STEP_1_HOUR, "1 hour"),
                (STEP_1_DAY, "1 day"))


def now():
    return datetime.utcnow()


def yesterday(start=None):
    if start is None:
        start = now()
    return start - timedelta(days=1)


def last_week(start=None):
    if start is None:
        start = now()
    return start - timedelta(days=7)


def start_of_month(timestamp=None):
    if not timestamp:
        timestamp = now()
    return datetime(year=timestamp.year, month=timestamp.month, day=1)


def floor(start, resolution):
    """Floor a datetime by a resolution.

    >>> now = datetime(2012, 7, 6, 20, 33, 16, 573225)
    >>> floor(now, STEP_1_HOUR)
    datetime.datetime(2012, 7, 6, 20, 0)
    """
    if resolution == STEP_10_SEC:
        return datetime(start.year, start.month, start.day, start.hour,
                        start.minute, start.second - (start.second % 10))
    elif resolution == STEP_1_MIN:
        return datetime(start.year, start.month, start.day, start.hour,
                        start.minute)
    elif resolution == STEP_5_MIN:
        return datetime(start.year, start.month, start.day, start.hour,
                        start.minute - (start.minute % 5))
    elif resolution == STEP_1_HOUR:
        return datetime(start.year, start.month, start.day, start.hour)
    elif resolution == STEP_1_DAY:
        return datetime(start.year, start.month, start.day)

    raise ValueError("{resolution} is not a valid resolution. Valid choices "
                     "are {choices}".format(resolution=resolution,
                                            choices=STEP_CHOICES))


def _timedelta_total_seconds(td):
    """Python 2.6 backward compatibility function for timedelta.total_seconds.

    :type td: timedelta object
    :param td: timedelta object

    :rtype: float
    :return: The total number of seconds for the given timedelta object.

    """
    if hasattr(timedelta, "total_seconds"):
        return getattr(td, "total_seconds")()

    # Python 2.6 backward compatibility
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / float(10**6)


def _interval_string_to_seconds(interval_string):
    """Convert internal string like 1M, 1Y3M, 3W to seconds.

    :type interval_string: str
    :param interval_string: Interval string like 1M, 1W, 1M3W4h2s...
        (s => seconds, m => minutes, h => hours, D => days,
         W => weeks, M => months, Y => Years).

    :rtype: int
    :return: The conversion in seconds of interval_string.

    """
    interval_exc = "Bad interval format for {0}".format(interval_string)
    interval_dict = {"s": 1, "m": 60, "h": 3600, "D": 86400,
                     "W": 7*86400, "M": 30*86400, "Y": 365*86400}

    interval_regex = re.compile("^(?P<num>[0-9]+)(?P<ext>[smhDWMY])")
    seconds = 0

    while interval_string:
        match = interval_regex.match(interval_string)
        if match:
            num, ext = int(match.group("num")), match.group("ext")
            if num > 0 and ext in interval_dict:
                seconds += num * interval_dict[ext]
                interval_string = interval_string[match.end():]
            else:
                raise Exception(interval_exc)
        else:
            raise Exception(interval_exc)
    return seconds


def timeago(interval_string, start=None):
    if start is None:
        start = now()
    td = timedelta(seconds=_interval_string_to_seconds(interval_string))
    return start - td
