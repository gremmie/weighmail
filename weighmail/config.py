from ConfigParser import SafeConfigParser

from utils import make_label


DEFAULTS = dict(
    user=None,
    password=None,
    host='imap.gmail.com',
    ssl='True',
    port='993',
    labels=[],
)


def parse_config_file(path):
    """Parse INI file containing configuration details.

    """
    # Parse options file
    parser = SafeConfigParser(defaults=DEFAULTS)

    with open(path, 'r') as fp:
        parser.readfp(fp)

    # Build a list of label named tuples

    sections = [s for s in parser.sections() if s not in ('auth', 'connection')]

    labels = [make_label(sec,
                         parser.get(sec, 'min'),
                         parser.get(sec, 'max')) for sec in sections]

    # Build an options object and return it

    opts = dict(
        user=parser.get('auth', 'user'),
        password=parser.get('auth', 'password'),
        host=parser.get('connection', 'host'),
        ssl=parser.getboolean('connection', 'ssl'),
        port=parser.getint('connection', 'port'),
        labels=labels,
    )
    return opts
