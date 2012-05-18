from argparse import ArgumentParser
import getpass
import os.path
import sys

from config import parse_config_file, ConfigError


PROG_DESC = "Adds labels to your Gmail according to message size"


def parse_args():
    parser = ArgumentParser(description=PROG_DESC,
        epilog="Command-line arguments override config file settings.")

    default_config_file = os.path.expanduser(os.path.join('~',
        '.weighmail.ini'))
    parser.add_argument('-c', '--config', default=default_config_file,
            help="path to configuration file [default=%(default)s]")
    parser.add_argument('-u', '--user', help="user name")
    parser.add_argument('-p', '--password', help="password")
    parser.add_argument('-H', '--host', help="server name")
    parser.add_argument('-P', '--port', type=int, help="server port")
    parser.add_argument('-n', '--nossl', default=None, action='store_true',
            help="do not use SSL")

    args = parser.parse_args()

    # Remove items with a value of None, which indicates the user didn't specify
    # the option; this makes updating options from the config file easier:

    args = { k : v for k, v in vars(args).items() if v is not None }
    return args


def main():
    # Parse command-line arguments
    args = parse_args()

    config_file = args.pop('config')
    no_ssl = args.pop('nossl', False)

    # Read config file:
    opts = parse_config_file(config_file)

    # Command-line arguments override config file settings
    opts.update(args)

    if no_ssl:
        opts['ssl'] = False

    # If the user or password is not specified, prompt for them now
    for opt in ('user', 'password'):
        if opts[opt] is None:
            opts[opt] = getpass.getpass(opt + ': ')

    print opts


if __name__ == '__main__':
    try:
        main()
    except ConfigError, ex:
        sys.stderr.write("Configuration error: %s\n" % ex)
