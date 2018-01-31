# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import datetime
from unittest import TestCase

from i14y.util import prep_datetime, prep_tags


class PrepDatetimeTests(TestCase):
    def test_datetime_returns_isoformat(self):
        self.assertEqual(
            prep_datetime(datetime(2017, 1, 2, 3, 4, 5, 123456)),
            '2017-01-02T03:04:05.123456'
        )

    def test_none_returns_none(self):
        self.assertIsNone(prep_datetime(None))

    def test_non_datetime_raises_valueerror(self):
        with self.assertRaises(ValueError):
            prep_datetime('foo')


class PrepTagsTests(TestCase):
    def test_single_string_left_as_is(self):
        self.assertEqual(prep_tags('foo'), 'foo')

    def test_none_returns_none(self):
        self.assertIsNone(prep_tags(None))

    def test_list_of_strings_joined_by_comma(self):
        self.assertEqual(prep_tags(['foo', 'bar', 'baz']), 'foo,bar,baz')

    def test_sequence_of_strings_joined_by_comma(self):
        self.assertEqual(prep_tags((str(i) for i in range(6))), '0,1,2,3,4,5')
