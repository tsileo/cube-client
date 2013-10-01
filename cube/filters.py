# -*- encoding: utf-8 -*-

"""
Copyright (c) 2012 Steven Buss
Originally from:
https://github.com/sbuss/pypercube/blob/master/pypercube/filters.py
"""

import json


class Filter(object):
    """A filter for a cube event query."""
    def __init__(self, type, property_name, value):
        """Create a Filter.

        :param type: The type of the filter, eg "eq" or "gt".
        :type type: str
        :param property_name: The name of property on which to filter.
        :type property_name: str
        :param value: The value to which the property will be compared.
        :type value: str or list(str)
        """
        self.type = type
        self.property_name = property_name
        self.value = value

    def __repr__(self):
        return "<{name}: {value}>".format(name=self.__class__.__name__,
                                          value=self)

    def __str__(self):
        return ".{type}({property}, {value})".format(
            type=self.type, property=self.property_name,
            value=json.dumps(self.value))

    def __eq__(self, other):
        return self.type == other.type and \
            self.property_name == other.property_name and \
            self.value == other.value


class EQ(Filter):
    """An "equals" filter"""
    def __init__(self, property_name, value):
        return super(EQ, self).__init__("eq", property_name, value)


class LT(Filter):
    """A "less than" filter"""
    def __init__(self, property_name, value):
        return super(LT, self).__init__("lt", property_name, value)


class LE(Filter):
    """A "less than or equal to" filter"""
    def __init__(self, property_name, value):
        return super(LE, self).__init__("le", property_name, value)


class GT(Filter):
    """A "greater than" filter"""
    def __init__(self, property_name, value):
        return super(GT, self).__init__("gt", property_name, value)


class GE(Filter):
    """A "greater than or equal to" filter"""
    def __init__(self, property_name, value):
        return super(GE, self).__init__("ge", property_name, value)


class NE(Filter):
    """A "not equals" filter"""
    def __init__(self, property_name, value):
        return super(NE, self).__init__("ne", property_name, value)


class RE(Filter):
    """A "regular expression" filter"""
    def __init__(self, property_name, value):
        return super(RE, self).__init__("re", property_name, value)


class IN(Filter):
    """An "in array" filter"""
    def __init__(self, property_name, value):
        return super(IN, self).__init__("in", property_name,
                                        [x for x in value])


class StartsWith(RE):
    """A "starts with" filter"""
    def __init__(self, property_name, value):
        v = "^{value}".format(value=value)
        return super(StartsWith, self).__init__(property_name, v)


class EndsWith(RE):
    """An "ends with" filter"""
    def __init__(self, property_name, value):
        v = ".*{value}$".format(value=value)
        return super(EndsWith, self).__init__(property_name, v)
