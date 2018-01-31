from __future__ import absolute_import, unicode_literals

import six


class APIError(Exception):
    def __init__(self, message, status_code=None, response=None):
        self._message = message
        self.status_code = status_code
        self.response = response

    def __unicode__(self):
        return self._message

    if six.PY3:
        def __str__(self):
            return self.__unicode__()
    else:  # pragma: no cover
        def __str__(self):
            return unicode(self).encode('utf-8')


class APIConnectionError(APIError):
    pass


class DocumentAlreadyExistsError(APIError):
    pass


class InvalidRequestError(APIError):
    pass
