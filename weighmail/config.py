import collections
import re
from ConfigParser import SafeConfigParser


class ConfigError(Exception):
    pass


LIMIT_RE = re.compile(r'^(\d+)(GB|MB|KB)?$', re.IGNORECASE)

KB = 1024
MB = KB * KB
GB = MB * MB

SUFFIX_SIZES = {
    None: 1,
    'KB': KB,
    'MB': MB,
    'GB': GB
}


def parse_config_file(path):
    """Parse INI file containing configuration details.

    """
    # Parse options file
    defaults = dict(
        username=None,
        password=None,
        host='imap.gmail.com',
        ssl='True',
        port='993',
    )
    parser = SafeConfigParser(defaults=defaults, allow_no_value=True)

    with open(path, 'r') as fp:
        parser.readfp(fp)

    # Build a list of label named tuples
    Label = collections.namedtuple('Label', 'name min max')

    label_set = set(parser.sections()) - {'auth', 'connection'}
    if not label_set:
        raise ConfigError("please specify at least 1 label section")

    labels = []
    for label in label_set:
        min_val = get_limit(parser.get(label, 'min'))
        max_val = get_limit(parser.get(label, 'max'))

        if (min_val is not None and max_val is not None and 
                min_val > max_val):
            raise ConfigError("min is > max for label %s" % label)

        labels.append(Label(name=label, min=min_val, max=max_val))

    # Build an options object and return it
    fields = defaults.keys() + ['labels']
    Options = collections.namedtuple('Options', fields)

    opts = Options(
        username=parser.get('auth', 'username'),
        password=parser.get('auth', 'password'),
        host=parser.get('connection', 'host'),
        ssl=parser.getboolean('connection', 'ssl'),
        port=parser.getint('connection', 'port'),
        labels=labels,
    )
    return opts


def get_limit(val):
    """Turns a string limit (e.g. 3MB) into an integer"""

    # An empty string is OK, it means no limit, which we translate to None
    if val == '':
        return None

    match = LIMIT_RE.match(val)
    if match is None:
        raise ConfigError("invalid min/max value %s" % val)

    return int(match.group(1)) * SUFFIX_SIZES[match.group(2).upper()]

