# -*- encoding: utf-8 -*-
from cube.expression import EventExpression


class Event(object):
    """ Cube instance that hold an event_type,
    with shortcut for getting/creating events/metrics,
    and creating expression. """
    def __init__(self, cube, event_type):
        self.cube = cube
        self.event_type = event_type

    def put(self, event_data={}, **kwargs):
        return self.cube.put(self.event_type, event_data, **kwargs)

    def event(self, expression=None, **kwargs):
        if expression is None:
            expression = self.event_type
            return self.cube.event(expression, **kwargs)

    def metric(self, expression, **kwargs):
        return self.cube.metric(expression, **kwargs)

    def expression(self, event_properties):
        return EventExpression(self.event_type, event_properties)
