from __future__ import absolute_import, unicode_literals

import re

from i14y import Drawer
from i14y.error import InvalidRequestError
from i14y.indexer.mulcher import Mulcher


def url_to_document_id(url):
    """Convert a URL to a document ID usable with i14y.

    Replaces slashes, colons, and spaces with underscores.
    """
    return re.sub('[/: ]', '_', url)


class Indexer(object):
    """Indexer for creation, updating, and deletion of i14y documents.

    Requires either an i14y.Drawer object instance or a pair of (drawer_handle,
    secret_token) credentials that can be used to access an i14y drawer.
    """
    def __init__(self, drawer_handle=None, secret_token=None, drawer=None,
                 mulcher=None, document_id_fn=None):
        self.drawer = drawer or Drawer(
            drawer_handle=drawer_handle,
            secret_token=secret_token
        )

        self.mulcher = mulcher or Mulcher()
        self.document_id_fn = document_id_fn or url_to_document_id

    def create_document(self, url):
        self.drawer.create_document(
            document_id=self.document_id_fn(url),
            **self.mulcher.mulch(url)
        )

    def update_document(self, url):
        self.drawer.update_document(
            document_id=self.document_id_fn(url),
            **self.mulcher.mulch(url)
        )

    def update_or_create_document(self, url):
        mulched = self.mulcher.mulch(url)
        document_id = self.document_id_fn(url)

        try:
            self.drawer.update_document(document_id=document_id, **mulched)
        except InvalidRequestError:
            self.drawer.create_document(document_id=document_id, **mulched)

    def delete_document(self, url):
        document_id = self.document_id_fn(url)
        self.drawer.delete_document(document_id=document_id)
