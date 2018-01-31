from __future__ import absolute_import, unicode_literals

import json

from requests import Session

import i14y
from i14y.error import APIConnectionError, APIError, InvalidRequestError


class Client(object):
    def __init__(self, drawer_handle, secret_token, api_base=None):
        self.session = Session()

        if not drawer_handle or not secret_token:
            raise ValueError('must provide drawer_handle and secret_token')

        self.session.auth = (drawer_handle, secret_token)

        self.api_base = api_base or i14y.api_base

    def request(self, method, url, data=None):
        status_code, response = self._make_request(method, url, data=data)

        if not (200 <= status_code < 300):
            self._handle_error(status_code, response)

        return response

    def _make_request(self, method, url, data=None):
        full_url = '%s%s' % (self.api_base, url)

        if data:
            # Use ensure_ascii=False to keep unicode characters.
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')

        try:
            response = self.session.request(method, full_url, data=data)
            status_code = response.status_code
            content = response.json()

            return status_code, content
        except Exception as e:
            message = 'Unexpected error communicating with the i14y API.'
            message += '\n\n%s: %s' % (type(e).__name__, str(e))
            raise APIConnectionError(message)

    def _handle_error(self, status_code, response):
        error = response.get('developer_message')

        if (400 <= status_code < 500):
            raise InvalidRequestError(error, status_code, response)
        else:
            raise APIError(error, status_code, response)
