# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from mock import Mock
from unittest import TestCase

from i14y.error import InvalidRequestError
from i14y.indexer import Indexer, url_to_document_id


class UrlToDocumentIdTests(TestCase):
    def test_conversion(self):
        self.assertEqual(
            url_to_document_id('https://domain.url/foo/bar?a=Hi therë'),
            'https___domain.url_foo_bar?a=Hi_therë'
        )


class IndexerTests(TestCase):
    def setUp(self):
        self.url = 'https://domain.url/foo/bar?x=y'
        self.drawer = Mock()
        self.mulcher = Mock(mulch=Mock(return_value={
            'path': self.url,
            'title': 'My title',
            'content': 'My content',
        }))

    def test_create_document(self):
        indexer = Indexer(drawer=self.drawer, mulcher=self.mulcher)
        indexer.create_document(self.url)

        self.mulcher.mulch.assert_called_once_with(self.url)
        self.drawer.create_document.assert_called_once_with(
            document_id='https___domain.url_foo_bar?x=y',
            path=self.url,
            title='My title',
            content='My content'
        )

    def test_update_document(self):
        indexer = Indexer(drawer=self.drawer, mulcher=self.mulcher)
        indexer.update_document(self.url)

        self.mulcher.mulch.assert_called_once_with(self.url)
        self.drawer.update_document.assert_called_once_with(
            document_id='https___domain.url_foo_bar?x=y',
            path=self.url,
            title='My title',
            content='My content'
        )

    def test_update_or_create_document_already_exists(self):
        indexer = Indexer(drawer=self.drawer, mulcher=self.mulcher)
        indexer.update_or_create_document(self.url)
        self.drawer.update_document.assert_called_once()
        self.drawer.create_document.assert_not_called()

    def test_update_or_create_document_does_not_exist(self):
        self.drawer.update_document.side_effect = InvalidRequestError('error')
        indexer = Indexer(drawer=self.drawer, mulcher=self.mulcher)
        indexer.update_or_create_document(self.url)
        self.drawer.update_document.assert_called_once()
        self.drawer.create_document.assert_called_once()

    def test_delete_document(self):
        indexer = Indexer(drawer=self.drawer)
        indexer.delete_document(self.url)

        self.drawer.delete_document.assert_called_once_with(
            document_id='https___domain.url_foo_bar?x=y'
        )
