# -*- encoding: utf-8 -*-

"""
Copyright (c) 2012 Steven Buss
Originally from:
https://github.com/sbuss/pypercube/blob/master/pypercube/time_utils.py
"""

from datetime import datetime
from datetime import timedelta

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
            "are {choices}".format(
                resolution=resolution, choices=STEP_CHOICES))
