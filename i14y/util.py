from __future__ import absolute_import, unicode_literals

from datetime import datetime

import six


def prep_datetime(dt):
    """Prepare datetime for the i14y API.

    If the passed value is a Python datetime object, convert it to an ISO 8601
    string. If None, return None.  Otherwise raises a ValueError.
    """
    if isinstance(dt, datetime):
        return dt.isoformat()

    if dt is None:
        return None

    raise ValueError(dt)


def prep_tags(tags):
    """Prepare tags for the i14y API.

    If the passed value is a single string, return it as-is. If None, return
    None. Otherwise, treat the input as a sequence and join it with commas.
    """
    if isinstance(tags, six.string_types):
        return tags

    if tags is None:
        return None

    return ','.join(tags)
