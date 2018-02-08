from __future__ import absolute_import, unicode_literals

from unittest import TestCase

import requests
import responses

from i14y.indexer import Fetcher


class FetcherTests(TestCase):
    @responses.activate
    def test_retrieves_html(self):
        content = '<html>content</html>'
        url = 'https://some.url'
        responses.add(responses.GET, url, body=content)
        self.assertEqual(Fetcher().fetch(url), content)

    @responses.activate
    def test_raises_exception(self):
        url = 'https://some.error'
        responses.add(responses.GET, url, status=500, body='error')
        with self.assertRaises(requests.exceptions.RequestException):
            Fetcher().fetch(url)
