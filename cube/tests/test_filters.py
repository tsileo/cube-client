# -*- encoding: utf-8 -*-

"""
Copyright (c) 2012 Steven Buss
Originally from:
https://github.com/sbuss/pypercube/blob/master/tests/test_filters.py
"""

import unittest

from cube.filters import Filter
from cube.filters import EQ
from cube.filters import LT
from cube.filters import LE
from cube.filters import GT
from cube.filters import GE
from cube.filters import NE
from cube.filters import RE
from cube.filters import IN
from cube.filters import StartsWith
from cube.filters import EndsWith


class TestFilter(unittest.TestCase):
    def test_equality(self):
        f1 = Filter('eq', 'name', 'test')
        f2 = EQ('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('lt', 'name', 'test')
        self.assertNotEqual(f1, f2)
        f2 = LT('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('le', 'name', 'test')
        f2 = LE('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('gt', 'name', 'test')
        f2 = GT('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('ge', 'name', 'test')
        f2 = GE('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('ne', 'name', 'test')
        f2 = NE('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('re', 'name', 'test')
        f2 = RE('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('in', 'name', ['t', 'e', 's', 't'])
        f2 = IN('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('in', 'name', ['test'])
        f2 = IN('name', ['test'])
        self.assertEqual(f1, f2)
        f1 = Filter('re', 'name', '^test')
        f2 = StartsWith('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('re', 'name', '.*test$')
        f2 = EndsWith('name', 'test')
        self.assertEqual(f1, f2)

    def test_starts_with(self):
        f = StartsWith('name', 'test')
        self.assertEqual("%s" % f, '.re(name, "^test")')

    def test_ends_with(self):
        f = EndsWith('name', 'test')
        self.assertEqual("%s" % f, '.re(name, ".*test$")')

#    def test_re(self):
#        # FIXME: Regular expressions are broken
#        f = RE('name', r"\s+([A-Za-z0-9]+)")
#        self.assertEqual("%s" % f, r'.re(name, "\s+([A-Za-z0-9]+)")')

    def test_in(self):
        f = IN('name', ['a', 'b', 'c'])
        self.assertEqual("%s" % f, '.in(name, ["a", "b", "c"])')
