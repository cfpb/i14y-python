# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json
from unittest import TestCase

import responses

from i14y import error
from i14y.client import Client


class ClientTests(TestCase):
    def test_client_with_null_credentials_raises_valueerror(self):
        with self.assertRaises(ValueError):
            Client(drawer_handle=None, secret_token=None)

    def test_client_with_null_credential_raises_valueerror(self):
        with self.assertRaises(ValueError):
            Client(drawer_handle=None, secret_token='token')

    @responses.activate
    def test_client_request_uses_api_base(self):
        client = Client('handle', 'token', 'http://api.base')
        responses.add(responses.GET, 'http://api.base/foo', json={'x': 'y'})
        self.assertEqual(client.request('get', '/foo'), {'x': 'y'})

    @responses.activate
    def test_client_request_uses_basic_authentication(self):
        client = Client('handle', 'token', 'http://api.base')
        responses.add(responses.GET, 'http://api.base/foo', json={})
        client.request('get', '/foo')
        self.assertEqual(
            responses.calls[0].request.headers['Authorization'],
            'Basic aGFuZGxlOnRva2Vu'
        )

    @responses.activate
    def test_client_post_keeps_unicode_characters(self):
        def callback(request):
            data = json.loads(request.body)
            self.assertEqual(data['x'], 'ñ')
            return (200, {}, json.dumps({}))

        client = Client('handle', 'token', 'http://api.base')
        responses.add_callback(
            responses.POST,
            'http://api.base/foo',
            callback=callback
        )

        client.request('post', '/foo', data={'x': 'ñ'})

    @responses.activate
    def test_client_request_exceptions_raise_apierror(self):
        client = Client('handle', 'token', 'http://api.base')
        responses.add(
            responses.GET,
            'http://api.base/foo',
            body=ValueError('err')
        )

        try:
            client.request('get', '/foo')
        except error.APIConnectionError as e:
            self.assertEqual(str(e), (
                'Unexpected error communicating with the i14y API.\n\n'
                'ValueError: err'
            ))
        else:
            self.fail('request errors should raise APIConnectionError')

    @responses.activate
    def test_client_400_raises_invalidrequesterror(self):
        client = Client('handle', 'token', 'http://api.base')
        responses.add(responses.GET, 'http://api.base/x', status=400, json={})

        with self.assertRaises(error.InvalidRequestError):
            client.request('get', '/x')

    @responses.activate
    def test_client_500_raises_apierror(self):
        client = Client('handle', 'token', 'http://api.base')
        responses.add(responses.GET, 'http://api.base/x', status=500, json={})

        with self.assertRaises(error.APIError):
            client.request('get', '/x')
