# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from datetime import datetime
import json
from unittest import TestCase

import responses

from i14y.drawer import Drawer


class DrawerTests(TestCase):
    def setUp(self):
        self.drawer = Drawer(
            drawer_handle='handle',
            secret_token='token',
            api_base='http://api.base'
        )

    def test_instance_url_urlencodes_document_id(self):
        self.assertEqual(
            self.drawer.instance_url('El Niño'),
            '/documents/El%20Ni%C3%B1o'
        )

    def test_create_document_requires_content_or_description(self):
        with self.assertRaises(ValueError):
            self.drawer.create_document(
                document_id='foo',
                title='title',
                path='https://my.site/path'
            )

    @responses.activate
    def test_create_document(self):
        def callback(request):
            data = json.loads(request.body)

            self.assertEqual(data, {
                'document_id': 'foo',
                'title': 'title',
                'path': 'https://my.site/path',
                'created': '2017-01-02T03:04:05.123456',
                'description': 'descriptioñ',
                'content': 'conteñt',
                'promote': True,
                'language': 'en',
                'tags': 'foo,bar'
            })

            return (200, {}, json.dumps({}))

        responses.add_callback(
            responses.POST,
            'http://api.base/documents',
            callback=callback
        )

        self.drawer.create_document(
            document_id='foo',
            title='title',
            path='https://my.site/path',
            created=datetime(2017, 1, 2, 3, 4, 5, 123456),
            description='descriptioñ',
            content='conteñt',
            promote=True,
            language='en',
            tags=['foo', 'bar']
        )

    @responses.activate
    def test_update_document(self):
        def callback(request):
            data = json.loads(request.body)

            self.assertEqual(data, {
                'title': 'title',
                'path': 'https://my.site/path',
                'created': '2017-01-02T03:04:05.123456',
                'description': 'descriptioñ',
                'content': 'conteñt',
                'changed': '2017-02-03T04:05:06.234567',
                'language': 'en',
                'tags': 'baz'
            })

            return (200, {}, json.dumps({}))

        responses.add_callback(
            responses.PUT,
            'http://api.base/documents/foo',
            callback=callback
        )

        self.drawer.update_document(
            document_id='foo',
            title='title',
            path='https://my.site/path',
            created=datetime(2017, 1, 2, 3, 4, 5, 123456),
            description='descriptioñ',
            changed=datetime(2017, 2, 3, 4, 5, 6, 234567),
            content='conteñt',
            language='en',
            tags='baz'
        )

    @responses.activate
    def test_delete_document(self):
        responses.add(
            responses.DELETE,
            'http://api.base/documents/foo',
            json={'deleted': 'ok'}
        )

        self.assertEqual(
            self.drawer.delete_document('foo'),
            {'deleted': 'ok'}
        )
