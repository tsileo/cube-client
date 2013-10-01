===========
Cube-client
===========

A Python client for `Cube: Time Series Data Collection & Analysis <http://square.github.com/cube/>`_.

.. image:: https://pypip.in/v/cube-client/badge.png
        :target: https://crate.io/packages/cube-client

.. image:: https://pypip.in/d/cube-client/badge.png
        :target: https://crate.io/packages/cube-client


Features
========

You can post (`Collector <https://github.com/square/cube/wiki/Collector>`_) and request (`Evaluator <https://github.com/square/cube/wiki/Evaluator>`_) data to/from Cube.

- Post events
- Request events
- Request metrics
- Request known event types


Overview
========

.. code-block:: python

    >>> from cube import Cube, ONE_HOUR
    >>> c = Cube()
    >>> 
    >>> c.put('sample_data', {'myval': 10})
    [{'data': {'myval': 10}, 'type': 'sample_data', 'time': '2012-10-01T13:04:04.453929'}]

    >>> c.event('sample_data')
    [{u'time': u'2012-10-01T13:04:04.453Z'}]

    >>> c.put('sample_data', {'myval': 20})
    [{'data': {'myval': 20}, 'type': 'sample_data', 'time': '2012-10-01T13:04:39.725676'}]

    >>> c.event('sample_data')
    [{u'time': u'2012-10-01T13:04:04.453Z'}, {u'time': u'2012-10-01T13:04:39.725Z'}]

    >>> c.event('sample_data(myval)'')
    [{u'data': {u'myval': 10}, u'time': u'2012-10-01T13:04:04.453Z'}, {u'data': {u'myval': 20}, u'time': u'2012-10-01T13:04:39.725Z'}]

    >>> c.metric('sum(sample_data)', step=ONE_HOUR, start='2012-10-01')
    [{u'value': 0, u'time': u'2012-10-01T00:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T01:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T02:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T03:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T04:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T05:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T06:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T07:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T08:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T09:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T10:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T11:00:00.000Z'}, {u'value': 0, u'time': u'2012-10-01T12:00:00.000Z'}, {u'value': 2, u'time': u'2012-10-01T13:00:00.000Z'}]


Requirements
============

- `Requests <http://docs.python-requests.org/en/latest/>`_


Installation
============

::

    $ pip install cube-client


Usage
=====

.. code-block:: python

    from cube import Cube, ONE_HOUR
    from datetime import datetime

    cube = Cube()
    # or
    cube = Cube('localhost') 

    # Create an event
    cube.put("myevent", {'temp': 30})
    # or
    cube.put("myevent", {'temp': 30}, time=datetime.now().isoformat())

    # Low level queries
    # =================

    # Request events data
    # See Cube queries:
    # https://github.com/square/cube/wiki/Queries#wiki-metric
    cube.event('myevent(temp)')

    # Request metrics
    cube.metric('sum(myevent(temp))', step='36e5', start='2013-9-01'))
    # or
    cube.metric('sum(myevent(temp))', step=ONE_HOUR, start='2013-9-01'))

    # Request known event types
    cube.types()

    # High level queries
    # ==================

    from cube.expressions import EventExpression, Sum
    temp = EventExpression('myevent', 'temp')

    cube.metric(Sum(temp), step=ONE_HOUR, start='2013-10-1')


Metric resolutions shortcut
---------------------------

- **TEN_SECOND** for **1e4** - 10-second
- **ONE_MINUTE** for **6e4** - 1-minute 
- **FIVE_MINUTE** for **3e5** - 5-minute
- **ONE_HOUR** for **36e5** - 1-hour
- **ONE_DAY** for **864e5** - 1-day

::

    from cube import ONE_HOUR, FIVE_MINUTE

Time utils
----------



Event helper
------------

.. code-block:: python

    from cube import Cube, Event

    cube = Cube()

    my_event = cube.get_event('myevent')
    # or
    my_event = Event(cube, 'myevent')

    my_event.put({'temp': 10})
    my_event.put({'temp': 20})

    my_event.event()
    # [{u'time': u'2012-10-01T13:04:04.453Z'}, {u'time': u'2012-10-01T13:04:39.725Z'}]

    my_event.event('myevent(temp)')


Changelog
=========

0.2.0
-----

**Not released yet**

- Cleaned code (PEP8)
- Compatible with requests 2.0
- Added metric resolution shortcut
- Added a ``Event`` helper
- **Merged some parts of `sbuss/pypercube <https://github.com/sbuss/pypercube>`_**, ``time_utils``, ``EventExpression`` and ``Filter``.



License (MIT)
=============

Copyright (c) 2012 Thomas Sileo and Steven Buss

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.