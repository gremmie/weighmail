"""Common utilities for weighmail.

"""
import collections
import re


class AppError(Exception):
    pass


LIMIT_RE = re.compile(r'^(\d+)(GB|MB|KB)?$', re.IGNORECASE)

KB = 1024
MB = KB * KB
GB = MB * KB

SUFFIX_SIZES = {
    None: 1,
    'KB': KB,
    'MB': MB,
    'GB': GB
}

Label = collections.namedtuple('Label', 'name min max')


def make_label(name, min_str, max_str):
    """Make a Label object from 3 string parameters:

    name - label name
    min_str - minimum value, e.g. '5MB'
    max_str - maximum value, e.g. '10GB'

    Either min_str or max_str can be empty or None, in which
    case None will be used in the Label object.

    It is not valid to have None for both min and max.

    """
    min_val = get_limit(min_str)
    max_val = get_limit(max_str)

    if (min_val is not None and max_val is not None and
            min_val > max_val) or (min_val is None and max_val is None):
        raise ValueError("invalid label range: %s" % name)

    return Label(name, min_val, max_val)


def get_limit(val):
    """Turns a string limit (e.g. 3MB) into an integer

    An empty string or None will be translated to None.
    
    """
    if val is None or val == '':
        return None

    match = LIMIT_RE.match(val)
    if match is None:
        raise ValueError("invalid min/max value %s" % val)

    suffix = match.group(2).upper() if match.group(2) else None
    return int(match.group(1)) * SUFFIX_SIZES[suffix]
