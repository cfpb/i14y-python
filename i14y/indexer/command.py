from __future__ import absolute_import, unicode_literals

import argparse
import os
import sys

from i14y.indexer import Indexer


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Valid actions:

create - create a new document for a URL
update - update the existing document for a URL
update_or_create - try updating, fall back to creating
delete - delete the existing document for a URL"""
    )

    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='verbosity of debugging output')
    parser.add_argument('-d', '--drawer-handle', help=(
        'i14y drawer handle. Defaults to value of environment variable '
        'I14Y_DRAWER_HANDLE'
    ))
    parser.add_argument('-s', '--secret-token', help=(
        'i14y secret token. Defaults to value of environment variable '
        'I14Y_SECRET_TOKEN'
    ))
    parser.add_argument('action', help='action to take on a URL')
    parser.add_argument('url', help='full absolute URL')
    parser.add_argument('--html', type=argparse.FileType('r'), help=(
        'file containing HTML content for the specified URL'
    ))

    args = parser.parse_args()

    drawer_handle = args.drawer_handle or os.getenv('I14Y_DRAWER_HANDLE')
    if not drawer_handle:
        parser.error((
            'No drawer handle provided (use -d option or set the '
            'I14Y_DRAWER_HANDLE environment variable)'
        ))
        return 1

    secret_token = args.secret_token or os.getenv('I14Y_SECRET_TOKEN')
    if not secret_token:
        parser.error((
            'No secret token provided (use -s option or set the '
            'I14Y_SECRET_TOKEN environment variable)'
        ))
        return 1

    indexer = Indexer(drawer_handle=drawer_handle, secret_token=secret_token)

    if args.action == 'create':
        indexer.create_document(args.url, html_file=args.html)
    elif args.action == 'update':
        indexer.update_document(args.url, html_file=args.html)
    elif args.action == 'update_or_create':
        indexer.update_or_create_document(args.url, html_file=args.html)
    elif args.action == 'delete':
        indexer.delete_document(args.url)
    else:
        parser.error('Unsupported action: %s' % args.action)
        return 1


if __name__ == '__main__':
    sys.exit(main())
