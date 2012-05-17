from argparse import ArgumentParser
import os.path

from config import parse_config_file


PROG_DESC = "Adds labels to your Gmail according to message size"


def parse_args():
    parser = ArgumentParser(description=PROG_DESC,
        epilog="Command-line arguments override config file settings.")

    default_config_file = os.path.expanduser(os.path.join('~',
        '.weighmail.ini'))
    parser.add_argument('-c', '--config', default=default_config_file,
            help="path to configuration file [default=%(default)s]")
    parser.add_argument('-u', '--user', default=None,
            help="Gmail username")
    parser.add_argument('-p', '--password', default=None,
            help="Gmail password")
    parser.add_argument('-H', '--host', default='imap.gmail.com',
            help="Gmail server name [default=%(default)s]")
    parser.add_argument('-P', '--port', default=993, type=int,
            help="Gmail server port [default=%(default)s]")
    parser.add_argument('-n', '--nossl', action='store_true',
            help="do not use SSL [default=%(default)s]")

    args = parser.parse_args()
    print args
    print

def main():
    parse_args()
    opts = parse_config_file('weighmail.ini')
    print opts


if __name__ == '__main__':
    main()
