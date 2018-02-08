from __future__ import absolute_import, unicode_literals

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma nocover
    BeautifulSoup = None


class Mulcher(object):
    """Object that mulches HTML into content for the i14y API.

    Uses the Beautiful Soup 4 library to parse HTML.

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

    def mulch(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        mulched = {}

        title = soup.title.string.strip()
        if title:
            mulched['title'] = title

        description = soup.find('meta', attrs={'name': 'description'})
        if description and description.get('content'):
            mulched['description'] = description.get('content')

        content = soup.find('main')
        if content and content.text:
            mulched['content'] = content.text

        return mulched
