from unittest import TestCase

from mock import patch
import responses

from i14y.indexer import Mulcher


class MulcherTests(TestCase):
    def test_bs4_not_available_raises_runtimeerror(self):
        with patch('i14y.indexer.mulcher.BeautifulSoup', new=None):
            with self.assertRaises(RuntimeError):
                Mulcher()

    @responses.activate
    def test_mulch_using_requests(self):
        content = (
            '<html><head>'
            '<title>My title</title>'
            '<meta name="description" content="My description">'
            '</head><body>'
            '<header>Header</header>'
            '<main>Main content</main>'
            '<footer>Footer</footer>'
            '</body></html>'
        )

        responses.add(responses.GET, 'https://some.url', body=content)
        self.assertEqual(Mulcher().mulch('https://some.url'), {
            'path': 'https://some.url',
            'title': 'My title',
            'description': 'My description',
            'content': 'Main content',
        })

    @responses.activate
    def test_content_has_no_description(self):
        content = (
            '<html><head><title>My title</title></head><body>'
            '<header>Header</header>'
            '<main>Main content</main>'
            '<footer>Footer</footer>'
            '</body></html>'
        )

        responses.add(responses.GET, 'https://some.url', body=content)
        self.assertEqual(Mulcher().mulch('https://some.url'), {
            'path': 'https://some.url',
            'title': 'My title',
            'content': 'Main content',
        })

    @responses.activate
    def test_content_has_no_main(self):
        content = (
            '<html><head>'
            '<title>My title</title>'
            '<meta name="description" content="My description">'
            '</head><body>'
            '<header>Header</header>'
            '<footer>Footer</footer>'
            '</body></html>'
        )

        responses.add(responses.GET, 'https://some.url', body=content)
        self.assertEqual(Mulcher().mulch('https://some.url'), {
            'path': 'https://some.url',
            'title': 'My title',
            'description': 'My description',
        })
