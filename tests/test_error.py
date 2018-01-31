# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

import six

from i14y.error import APIError


class APIErrorTests(unittest.TestCase):
    @unittest.skipUnless(six.PY2, 'specific to Python 2')
    def test_formatting_ascii(self):
        self.assertEqual(str(APIError('foo')), 'foo')

    def test_formatting_unicode(self):
        err = APIError('unicodë')

        if six.PY3:
            self.assertEqual(str(err), 'unicodë')
        else:
            self.assertEqual(str(err), b'unicod\xc3\xab')
            self.assertEqual(unicode(err), 'unicodë')
