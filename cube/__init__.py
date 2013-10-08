# -*- encoding: utf-8 -*-
from datetime import datetime

try:
    import ujson as json
except ImportError:
    import json

import requests

from cube.expression import Sum, Min, Max, Median, Distinct
from cube.event import Event

API_VERSION = '1.0'

# Metric resolutions shortcuts
# From https://github.com/square/cube/wiki/Evaluator
TEN_SECOND = '1e4'
ONE_MINUTE = '6e4'
FIVE_MINUTE = '3e5'
ONE_HOUR = '36e5'
ONE_DAY = '864e5'


class Cube(object):
    def __init__(self, hostname="localhost", **kwargs):
        self.collector_url = 'http://{0}:{1}/{2}/'.format(hostname,
                                                          kwargs.get('collector_port', 1080),
                                                          API_VERSION)
        self.evaluator_url = 'http://{0}:{1}/{2}/'.format(hostname,
                                                          kwargs.get('evaluator_port', 1081),
                                                          API_VERSION)

    def put(self, event_type, event_data={}, **kwargs):
        """
        Create/update an event.
        """
        event = dict(type=event_type, data=event_data)

        event["time"] = kwargs.get("time", datetime.utcnow().isoformat())

        if kwargs.get("id"):
            event["id"] = kwargs.get("id")

        data = json.dumps([event])

        r = requests.post(self.collector_url + 'event/put',
                          data=data,
                          headers={'content-type': 'application/json'})
        r.raise_for_status()

        return [event]

    def make_query(self, query_type, expression, **kwargs):
        """
        Actually perform the query,
        try to convert datetime to isoformat on the fly
        """
        data = dict(expression=str(expression),
                    stop=kwargs.get('stop', datetime.utcnow()))
        data.update(kwargs)

        for k in ['start', 'stop']:
            if k in data:
                try:
                    data[k] = data[k].isoformat()
                except AttributeError:
                    pass

        r = requests.get(self.evaluator_url + query_type, params=data)
        r.raise_for_status()

        return r.json()

    def event(self, expression, **kwargs):
        """
        Query with an event expression
        """
        return self.make_query('event', expression, **kwargs)

    def metric(self, expression, **kwargs):
        """
        Query with a metric expression
        """
        return self.make_query('metric', expression, **kwargs)

    def types(self):
        """
        List of the known event types
        """
        r = requests.get(self.evaluator_url + 'types')
        r.raise_for_status()
        return r.json()

    def get_event(self, event_type):
        """
        Shortcut to initialize an Event object
        """
        return Event(self, event_type)
