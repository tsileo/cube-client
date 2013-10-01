# -*- encoding: utf-8 -*-

"""
Copyright (c) 2012 Steven Buss
Originally from:
https://github.com/sbuss/pypercube/blob/master/tests/test_metric_expression.py
"""

import unittest

from cube.expression import (Distinct, EventExpression,
                             Max, Median, MetricExpression, Min, Sum)


class TestMetricExpressions(unittest.TestCase):
    def setUp(self):
        self.e = EventExpression('request')

    def _test_op(self, op_str, op):
        m1 = MetricExpression(op_str, self.e)
        m2 = op(self.e)
        self.assertEqual(m1, m2)
        s = "{op}(request)".format(op=op_str)
        self.assertEqual("%s" % m1, s)
        self.assertEqual("%s" % m2, s)

    def test_sum(self):
        self._test_op("sum", Sum)

    def test_min(self):
        self._test_op("min", Min)

    def test_max(self):
        self._test_op("max", Max)

    def test_median(self):
        self._test_op("median", Median)

    def test_distinct(self):
        self._test_op("distinct", Distinct)

    def test_equality(self):
        e1 = EventExpression('request')
        m1 = MetricExpression('sum', e1)
        m2 = MetricExpression('sum', e1)
        self.assertEqual(m1, m2)

        e2 = EventExpression('other')
        m2 = MetricExpression('sum', e2)
        self.assertNotEqual(m1, m2)

        m1 = MetricExpression('sum', e2)
        self.assertEqual(m1, m2)

        m1 = MetricExpression('min', e2)
        self.assertNotEqual(m1, m2)

        m2 = MetricExpression('min', e2)
        self.assertEqual(m1, m2)

    def test_invalid_params(self):
        self.assertRaisesRegexp(ValueError,
                "Events for Metrics may only select a single event property",
                Sum, EventExpression('request', ['path', 'user_id']))
        self.assertRaises(TypeError, Sum)

    def test_filters(self):
        e1 = EventExpression('request', 'elapsed_ms').eq('path', '/')
        e2 = e1.gt('elapsed_ms', 500)
        self.assertEqual("%s" % Sum(e1),
                "sum(request(elapsed_ms).eq(path, \"/\"))")
        self.assertEqual("%s" % Sum(e2),
                "sum(request(elapsed_ms).eq(path, \"/\").gt(elapsed_ms, 500))")
