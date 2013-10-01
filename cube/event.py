# -*- encoding: utf-8 -*-


class Event(object):
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
        return self.cube.metric(self, expression, **kwargs)
