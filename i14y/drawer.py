from __future__ import absolute_import, unicode_literals

from six.moves.urllib.parse import quote

from i14y import util
from i14y.client import Client


class Drawer(Client):
    @classmethod
    def class_url(cls):
        return '/documents'

    def instance_url(self, document_id):
        return '%s/%s' % (
            self.class_url(),
            quote(document_id.encode('utf-8'))
        )

    def create_document(self, document_id, title, path, created=None,
                        description=None, content=None, promote=None,
                        language=None, tags=None):
        """Create a new document given its document_id and attributes.

        Both title and path are required, as are at least one of description
        and content.
        """
        if not description and not content:
            raise ValueError(
                'must provide at least one of description, content'
            )

        data = self._make_document_data(
            title=title,
            path=path,
            created=util.prep_datetime(created),
            description=description,
            content=content,
            promote=promote,
            language=language,
            tags=util.prep_tags(tags)
        )

        data['document_id'] = document_id

        return self.request('post', self.class_url(), data=data)

    def update_document(self, document_id, title=None, path=None, created=None,
                        description=None, content=None, changed=None,
                        promote=None, language=None, tags=None):
        """Update a document given its document_id and changed attributes."""
        data = self._make_document_data(
            title=title,
            path=path,
            created=util.prep_datetime(created),
            description=description,
            content=content,
            changed=util.prep_datetime(changed),
            promote=promote,
            language=language,
            tags=util.prep_tags(tags)
        )

        return self.request('put', self.instance_url(document_id), data=data)

    def delete_document(self, document_id):
        """Delete a document given its document_id."""
        return self.request('delete', self.instance_url(document_id))

    def _make_document_data(self, **params):
        return {k: v for k, v in params.items() if v is not None}
