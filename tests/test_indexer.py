# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from unittest import TestCase

from mock import Mock
from six import StringIO

from i14y.error import InvalidRequestError
from i14y.indexer import Indexer, url_to_document_id


class UrlToDocumentIdTests(TestCase):
    def test_conversion(self):
        self.assertEqual(
            url_to_document_id('https://domain.url/foo/bar?a=Hi therë'),
            'https___domain.url_foo_bar?a=Hi_therë'
        )


class MockFetcher(object):
    def fetch(self, url):
        return (
            '<html><head>'
            '<title>My title</title>'
            '<meta name="description" content="My description">'
            '</head><body>'
            '<header>Header</header>'
            '<main>Main contënt</main>'
            '<footer>Footer</footer>'
            '</body></html>'
        )


class IndexerTests(TestCase):
    def setUp(self):
        self.url = 'https://domain.url/foo/bar?x=y'
        self.fetcher = MockFetcher()
        self.drawer = Mock()

    def test_create_document(self):
        indexer = Indexer(drawer=self.drawer, fetcher=self.fetcher)
        indexer.create_document(self.url)

        self.drawer.create_document.assert_called_once_with(
            document_id='https___domain.url_foo_bar?x=y',
            path=self.url,
            title='My title',
            description='My description',
            content='Main contënt'
        )

    def test_create_document_with_html_file(self):
        html_file = StringIO(
            '<html><head><title>Title in file</title></head>'
            '<body><main>Content in file</main></body></html>'
        )

        indexer = Indexer(drawer=self.drawer, fetcher=self.fetcher)
        indexer.create_document(self.url, html_file=html_file)

        self.drawer.create_document.assert_called_once_with(
            document_id='https___domain.url_foo_bar?x=y',
            path=self.url,
            title='Title in file',
            content='Content in file'
        )

    def test_update_document(self):
        indexer = Indexer(drawer=self.drawer, fetcher=self.fetcher)
        indexer.update_document(self.url)

        self.drawer.update_document.assert_called_once_with(
            document_id='https___domain.url_foo_bar?x=y',
            path=self.url,
            title='My title',
            description='My description',
            content='Main contënt'
        )

    def test_update_or_create_document_already_exists(self):
        indexer = Indexer(drawer=self.drawer, fetcher=self.fetcher)
        indexer.update_or_create_document(self.url)
        self.drawer.update_document.assert_called_once()
        self.drawer.create_document.assert_not_called()

    def test_update_or_create_document_does_not_exist(self):
        self.drawer.update_document.side_effect = InvalidRequestError('error')
        indexer = Indexer(drawer=self.drawer, fetcher=self.fetcher)
        indexer.update_or_create_document(self.url)
        self.drawer.update_document.assert_called_once()
        self.drawer.create_document.assert_called_once()

    def test_delete_document(self):
        indexer = Indexer(drawer=self.drawer)
        indexer.delete_document(self.url)

        self.drawer.delete_document.assert_called_once_with(
            document_id='https___domain.url_foo_bar?x=y'
        )
