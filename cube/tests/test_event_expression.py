# -*- encoding: utf-8 -*-

"""
Copyright (c) 2012 Steven Buss
Originally from:
https://raw.github.com/sbuss/pypercube/master/tests/test_event_expression.py
"""

import unittest

from cube.expression import EventExpression


class TestEventExpressions(unittest.TestCase):
    def test_copy(self):
        e1 = EventExpression('request', ['path', 'elapsed_ms'])
        e2 = e1.copy()
        self.assertEqual(e1, e2)
        e1 = e1.eq('path', '/')
        e3 = e1.copy()
        self.assertNotEqual(e1, e2)
        self.assertEqual(e1, e3)
        self.assertNotEqual(e2, e3)

    def test_equality(self):
        e1 = EventExpression('request')
        e2 = EventExpression('request')
        self.assertEqual(e1, e2)
        e1 = EventExpression('request', 'path')
        self.assertNotEqual(e1, e2)
        e2 = EventExpression('request', 'path')
        self.assertEqual(e1, e2)
        e1 = EventExpression('request', ['path', 'elapsed_ms'])
        self.assertNotEqual(e1, e2)
        e2 = EventExpression('request', ['path', 'elapsed_ms'])
        self.assertEqual(e1, e2)
        e1 = EventExpression('request', ['path', 'elapsed_ms']).eq('path', '/')
        self.assertNotEqual(e1, e2)
        e2 = EventExpression('request', ['path', 'elapsed_ms']).eq('path', '/')
        self.assertEqual(e1, e2)
        e1 = EventExpression('request', ['path', 'elapsed_ms']).eq(
            'path', '/').gt('elapsed_ms', 500)
        self.assertNotEqual(e1, e2)
        e2 = EventExpression('request', ['path', 'elapsed_ms']).eq(
            'path', '/').gt('elapsed_ms', 500)
        self.assertEqual(e1, e2)

    def _test_filter(self, filter_str):
        e = EventExpression('test')
        self.assertTrue(hasattr(e, filter_str))
        f = getattr(e, filter_str)
        filtered = f('elapsed_ms', 500)
        self.assertTrue(isinstance(filtered, EventExpression))
        self.assertTrue(len(filtered.filters), 1)
        self.assertEqual("%s" % filtered,
                "test.{filter_str}(elapsed_ms, 500)".format(
                    filter_str=filter_str))

    def test_eq(self):
        self._test_filter('eq')

    def test_lt(self):
        self._test_filter('lt')

    def test_le(self):
        self._test_filter('le')

    def test_gt(self):
        self._test_filter('gt')

    def test_ge(self):
        self._test_filter('ge')

    def test_ne(self):
        self._test_filter('ne')

    def test_re(self):
        self._test_filter('re')

    def test_startswith(self):
        e = EventExpression('test')
        f = e.startswith('foo', 'bar')
        self.assertEqual("%s" % f, 'test.re(foo, "^bar")')

    def test_endswith(self):
        e = EventExpression('test')
        f = e.endswith('foo', 'bar')
        self.assertEqual("%s" % f, 'test.re(foo, ".*bar$")')

    def test_contains(self):
        e = EventExpression('test')
        f = e.contains('foo', 'bar')
        self.assertEqual("%s" % f, 'test.re(foo, ".*bar.*")')

    def test_in_array(self):
        e = EventExpression('test')
        f = e.in_array('foo', ['bar', 'baz'])
        self.assertEqual("%s" % f, 'test.in(foo, ["bar", "baz"])')

        f = e.in_array('foo', 'bar')
        self.assertEqual("%s" % f, 'test.in(foo, ["b", "a", "r"])')

    def test_filter_chaining(self):
        e = EventExpression('test')
        e = e.eq('bar', 'baz')
        self.assertTrue(isinstance(e, EventExpression))
        self.assertEqual(len(e.filters), 1)
        e = e.lt('fizz', 'bang')
        self.assertTrue(isinstance(e, EventExpression))
        self.assertEqual(len(e.filters), 2)
        e = e.ge('foo', 4)
        self.assertTrue(isinstance(e, EventExpression))
        self.assertEqual(len(e.filters), 3)
        self.assertEqual("%s" % e,
                'test.eq(bar, "baz").lt(fizz, "bang").ge(foo, 4)')
