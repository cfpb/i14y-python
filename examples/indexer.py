from i14y.indexer import Indexer


indexer = Indexer(
    drawer_handle='my-drawer-handle',
    secret_token='my-secret-token'
)

indexer.create_document('https://www.usa.gov/')

indexer.update_document('https://www.usa.gov/')

indexer.update_or_create_document('https://www.usa.gov/')

indexer.delete_document('https://www.usa.gov/')
