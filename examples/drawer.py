# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import i14y


drawer = i14y.Drawer(
    drawer_handle='my-drawer-handle',
    secret_token='my-secret-token'
)

drawer.create_document(
    document_id='my-test-document',
    title='My document title',
    path='https://testing.example/my/test/document',
    content='i14y is grate!'
)

drawer.update_document(
    document_id='my-test-document',
    content='i14y is great!'
)

drawer.delete_document(document_id='my-test-document')
