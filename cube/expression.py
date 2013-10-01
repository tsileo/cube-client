# -*- encoding: utf-8 -*-

"""
Copyright (c) 2012 Steven Buss
Originally from:
https://github.com/sbuss/pypercube/blob/master/pypercube/expression.py
"""

import types

from cube import filters


class CompoundMetricExpression(object):
    """CompoundMetricExpressions have two MetricExpressions and an operator.

    Used to do calculated metrics like sum(request(elapsed_ms)) / sum(request)
    """
    def __init__(self, metric1, operator=None, metric2=None):
        """Create a CompoundMetricExpression.

        :param metric1: The metric on the left side of the operator
        :type metric1: `MetricExpression` or `CompoundMetricExpression`
        :param operator: The operator to use on metric1 and metric2
        :type operator: `str`
        :param metric2: The metric on the right side of the operator
        :type metric2: `MetricExpression` or `CompoundMetricExpression`

        Note that CompoundMetricExpression does respect standard order of
        operations (*/+-).

        >>> e = EventExpression('request')
        >>> m = MetricExpression('sum', e)
        >>> print(m + m)
        (sum(request) + sum(request))
        >>> print(m + m - m)
        ((sum(request) + sum(request)) - sum(request))
        >>> print(m + m * 2)
        (sum(request) + (sum(request) * 2))
        >>> print(m + m * m / m)
        (sum(request) + ((sum(request) * sum(request)) / sum(request)))
        """
        if not operator and metric2:
            raise ValueError("You must have an operator if metric2 is"
                "defined.")
        self.metric1 = metric1
        self.operator = operator
        self.metric2 = metric2

    def __eq__(self, other):
        """Note that this tests for *equality* not *equivalence*, eg
        m + (m + m) != (m + m) + m, though the two expressions are equivalent.
        """
        return self.metric1 == other.metric1 and \
                self.operator == other.operator and \
                self.metric2 == other.metric2

    def __str__(self):
        response = "%s" % self.metric1
        if self.operator and self.metric2:
            response = "(" + response
            response += " {op} {right})".format(
                    op=self.operator,
                    right=self.metric2)
        return response

    def __add__(self, right):
        """
        >>> e = EventExpression('request')
        >>> m = MetricExpression('sum', e)
        >>> print(m + m)
        (sum(request) + sum(request))
        """
        return CompoundMetricExpression(self, "+", right)

    def __sub__(self, right):
        """
        >>> e = EventExpression('request')
        >>> m = MetricExpression('sum', e)
        >>> print(m - m)
        (sum(request) - sum(request))
        """
        return CompoundMetricExpression(self, "-", right)

    def __mul__(self, right):
        """
        >>> e = EventExpression('request')
        >>> m = MetricExpression('sum', e)
        >>> print(m * m)
        (sum(request) * sum(request))
        """
        return CompoundMetricExpression(self, "*", right)

    def __div__(self, right):
        """
        >>> e = EventExpression('request')
        >>> m = MetricExpression('sum', e)
        >>> print(m / m)
        (sum(request) / sum(request))
        """
        return CompoundMetricExpression(self, "/", right)

    def __truediv__(self, right):
        return self.__div__(right)


class MetricExpression(object):
    """A single MetricExpression."""
    def __init__(self, metric_type, event_expression):
        """Calculate a Cube Metric.

        :param metric_type: The type of the metric, like 'sum' or 'min'
        :type metric_type: `str`
        :param event_expression: The EventExpression over which to calculate
        :type event_expression: `EventExpression`

        Note that the EventExpressions for Cube metrics may only have *one*
        event_property.

        >>> e = EventExpression('request')
        >>> print(MetricExpression('sum', e))
        sum(request)
        >>> e = EventExpression('request', 'elapsed_ms')
        >>> print(MetricExpression('sum', e))
        sum(request(elapsed_ms))
        """
        if len(event_expression.event_properties) > 1:
            raise ValueError("Events for Metrics may only select a single "
                    "event property")
        self.metric_type = metric_type
        self.event_expression = event_expression

    def __str__(self):
        return "{type}({value})".format(
                type=self.metric_type,
                value=self.event_expression)

    def __add__(self, right):
        return CompoundMetricExpression(self) + right

    def __sub__(self, right):
        return CompoundMetricExpression(self) - right

    def __mul__(self, right):
        return CompoundMetricExpression(self) * right

    def __div__(self, right):
        return CompoundMetricExpression(self).__div__(right)

    def __truediv__(self, right):
        return CompoundMetricExpression(self).__truediv__(right)

    def __eq__(self, other):
        """
        >>> e1 = EventExpression('request')
        >>> m1 = MetricExpression('sum', e1)
        >>> m2 = MetricExpression('sum', e1)
        >>> m1 == m2
        True
        """
        return self.metric_type == other.metric_type and \
                self.event_expression == other.event_expression


class Sum(MetricExpression):
    """A "sum" metric."""
    def __init__(self, event):
        super(Sum, self).__init__("sum", event)


class Min(MetricExpression):
    """A "min" metric."""
    def __init__(self, event):
        super(Min, self).__init__("min", event)


class Max(MetricExpression):
    """A "max" metric."""
    def __init__(self, event):
        super(Max, self).__init__("max", event)


class Median(MetricExpression):
    """A "median" metric."""
    def __init__(self, event):
        super(Median, self).__init__("median", event)


class Distinct(MetricExpression):
    """A "distinct" metric."""
    def __init__(self, event):
        super(Distinct, self).__init__("distinct", event)


class EventExpression(object):
    def __init__(self, event_type, event_properties=None):
        """Create an Event expression.

        :param event_type: The type of the event to query for.
        :type event_type: str
        :param event_properties: Any properties to fetch from the event.
        :type event_properties: `str` or `list(str)`

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> print(request_time.event_type)
        request
        >>> print(request_time.event_properties)
        ['elapsed_ms']
        >>> print(request_time.eq('path', '/').gt('elapsed_ms', 100).lt(
        ...     'elapsed_ms', 1000))  # doctest:+NORMALIZE_WHITESPACE
        request(elapsed_ms).eq(path, "/").gt(elapsed_ms, 100).lt(elapsed_ms,
                1000)
        """
        self.event_type = event_type
        if event_properties:
            if isinstance(event_properties, types.StringTypes):
                event_properties = [event_properties]
        else:
            event_properties = []
        self.event_properties = event_properties
        self.filters = []

    def copy(self):
        c = EventExpression(self.event_type, self.event_properties[:])
        c.filters = self.filters[:]
        return c

    def __eq__(self, other):
        """
        >>> e1 = EventExpression('request')
        >>> e2 = EventExpression('request')
        >>> e1 == e2
        True
        >>> e1 = EventExpression('request', 'path')
        >>> e1 == e2
        False
        """
        return self.event_type == other.event_type and \
                len(self.event_properties) == len(other.event_properties) and \
                all((x == y) for (x, y) in \
                    zip(self.event_properties, other.event_properties)) and \
                self.event_properties == other.event_properties and \
                len(self.filters) == len(other.filters) and \
                all((x == y) for (x, y) in zip(self.filters, other.filters))

    def eq(self, event_property, value):
        """An equals filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.eq('path', '/')
        >>> print(filtered)
        request(elapsed_ms).eq(path, "/")
        """
        c = self.copy()
        c.filters.append(filters.EQ(event_property, value))
        return c

    def ne(self, event_property, value):
        """A not-equal filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.ne('path', '/')
        >>> print(filtered)
        request(elapsed_ms).ne(path, "/")
        """
        c = self.copy()
        c.filters.append(filters.NE(event_property, value))
        return c

    def lt(self, event_property, value):
        """A less-than filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.lt('elapsed_ms', 500)
        >>> print(filtered)
        request(elapsed_ms).lt(elapsed_ms, 500)
        """
        c = self.copy()
        c.filters.append(filters.LT(event_property, value))
        return c

    def le(self, event_property, value):
        """A less-than-or-equal-to filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.le('elapsed_ms', 500)
        >>> print(filtered)
        request(elapsed_ms).le(elapsed_ms, 500)
        """
        c = self.copy()
        c.filters.append(filters.LE(event_property, value))
        return c

    def gt(self, event_property, value):
        """A greater-than filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.gt('elapsed_ms', 500)
        >>> print(filtered)
        request(elapsed_ms).gt(elapsed_ms, 500)
        """
        c = self.copy()
        c.filters.append(filters.GT(event_property, value))
        return c

    def ge(self, event_property, value):
        """A greater-than-or-equal-to filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.ge('elapsed_ms', 500)
        >>> print(filtered)
        request(elapsed_ms).ge(elapsed_ms, 500)
        """
        c = self.copy()
        c.filters.append(filters.GE(event_property, value))
        return c

    def re(self, event_property, value):
        """A regular expression filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.re('path', '[^A-Za-z0-9+]')
        >>> print(filtered)
        request(elapsed_ms).re(path, "[^A-Za-z0-9+]")
        """
        c = self.copy()
        c.filters.append(filters.RE(event_property, value))
        return c

    def startswith(self, event_property, value):
        """A starts-with filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.startswith('path', '/cube')
        >>> print(filtered)
        request(elapsed_ms).re(path, "^/cube")
        """
        c = self.copy()
        c.filters.append(filters.RE(event_property, "^{value}".format(
            value=value)))
        return c

    def endswith(self, event_property, value):
        """An ends-with filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.endswith('path', 'event/get')
        >>> print(filtered)
        request(elapsed_ms).re(path, ".*event/get$")
        """
        c = self.copy()
        c.filters.append(filters.RE(event_property, ".*{value}$".format(
            value=value)))
        return c

    def contains(self, event_property, value):
        """A string-contains filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.contains('path', 'event')
        >>> print(filtered)
        request(elapsed_ms).re(path, ".*event.*")
        """
        c = self.copy()
        c.filters.append(filters.RE(event_property, ".*{value}.*".format(
            value=value)))
        return c

    def in_array(self, event_property, value):
        """An in-array filter chain.

        >>> request_time = EventExpression('request', 'elapsed_ms')
        >>> filtered = request_time.in_array('path', '/event')
        >>> print(filtered)
        request(elapsed_ms).in(path, ["/", "e", "v", "e", "n", "t"])
        >>> filtered = request_time.in_array('path', ['/event', '/'])
        >>> print(filtered)
        request(elapsed_ms).in(path, ["/event", "/"])
        """
        c = self.copy()
        c.filters.append(filters.IN(event_property, value))
        return c

    def get_expression(self):
        event_type = self.event_type
        event_property = self.event_properties
        filters = self.filters

        expression = "{event_type}".format(event_type=event_type)

        if event_property:
            if isinstance(event_property, types.StringTypes):
                p = event_property
            else:
                p = ", ".join(str(x) for x in event_property)

            expression += "({properties})".format(properties=p)

        if filters:
            expression += "".join(str(filter) for filter in filters)
        return expression

    def __repr__(self):
        return "<EventExpression: {value}>".format(value=self)

    def __str__(self):
        return self.get_expression()
