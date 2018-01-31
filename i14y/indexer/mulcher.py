from __future__ import absolute_import, unicode_literals

import requests

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma nocover
    BeautifulSoup = None


class Mulcher(object):
    """Object that fetches a URL and prepares its content for the i14y API.

    Uses the requests library to retrive content and the Beautiful Soup 4
    library to parse that content.

    Uses the <title> tag for the document title.

    Looks for a <meta name="description" content="Some description"> tag for
    the document description.

    Looks for a <main> tag for the document content.
    """
    def __init__(self):
        if not BeautifulSoup:
            raise RuntimeError((
                "Use of this mulcher requires the Beautiful Soup 4 library "
                " (try 'pip install bs4')"
            ))

    def mulch(self, url):
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')

        mulched = {
            'path': url,
            'title': soup.title.string.strip(),
        }

        description = soup.find('meta', attrs={'name': 'description'})
        if description:
            mulched['description'] = description.get('content')

        content = soup.find('main')
        if content:
            mulched['content'] = content.text

        return mulched
