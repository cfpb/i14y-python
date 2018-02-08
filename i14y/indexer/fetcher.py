from __future__ import absolute_import, unicode_literals

import requests


class Fetcher(object):
    """Object that fetches HTML from a URL using the requests library."""
    def fetch(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text
