import argparse
import getpass
import sys

import imapclient

import config
from utils import make_label, AppError
from observers.console import ConsoleObserver
from core import weighmail


PROG_DESC = "Adds labels to your Gmail according to message size"
HELP_EPILOG = """Command-line arguments override config file settings.

A simple example to label messages between 1 and 5 MB as "big" and
messages over 5 MB as "huge":

$ %(prog)s --labels big:1MB-5MB huge:5MB-
 
"""


class LabelAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):

        labels = getattr(namespace, self.dest)
        for value in values:
            try:
                label = self.parse_label(value)
            except ValueError, ex:
                parser.error(ex)
            else:
                labels.append(label)

    def parse_label(self, value):
        name, size_range = value.split(':')
        min_size, max_size = size_range.split('-')
        return make_label(name, min_size, max_size)
                

def parse_args():
    parser = argparse.ArgumentParser(description=PROG_DESC, epilog=HELP_EPILOG,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-c', '--config', help="path to configuration file")
    parser.add_argument('-f', '--folder',
            help="mail folder to search [default: All Mail]")
    parser.add_argument('-u', '--user',
            help="user name [default: prompted]")
    parser.add_argument('-p', '--password',
            help="password [default: prompted]")
    parser.add_argument('-H', '--host',
            help="server name [default: imap.gmail.com]")
    parser.add_argument('-P', '--port', type=int,
            help="server port [default: 993]")
    parser.add_argument('-n', '--nossl', default=None, action='store_true',
            help="do not use SSL [default: SSL is used]")
    parser.add_argument('-l', '--labels', default=[], nargs='+',
            action=LabelAction, help="label specification: name:min-max")

    args = parser.parse_args()

    # Remove items that eval to False which indicates the user didn't specify
    # the option; this makes updating options from the config file easier:

    args = { k : v for k, v in vars(args).items() if v }
    return args


def create_imap_client(host, port, ssl, user, password):
    """Creates & returns an instance of an IMAPClient"""

    print "Connecting..."

    client = imapclient.IMAPClient(host=host, port=port, ssl=ssl)
    client.login(username=user, password=password)

    print "Connected."
    return client


def main():
    # Parse command-line arguments
    args = parse_args()

    config_file = args.pop('config', None)
    no_ssl = args.pop('nossl', False)

    # Read config file if the option was specified
    if config_file is not None:
        opts = config.parse_config_file(config_file)
    else:
        opts = config.DEFAULTS

    # Command-line arguments override config file settings
    opts.update(args)

    if no_ssl:
        opts['ssl'] = False

    # Check for label rules
    if 'labels' not in opts or not opts['labels']:
        raise AppError("Please specify some label definitions")

    # If the user or password is not specified, prompt for them now
    for opt in ('user', 'password'):
        if opt not in opts or opts[opt] is None:
            opts[opt] = getpass.getpass(opt + ': ')

    imap_args = opts.copy()
    del imap_args['folder']
    del imap_args['labels']

    client = create_imap_client(**imap_args)
    observer = ConsoleObserver()

    weighmail(client, opts['folder'], opts['labels'], observer)
    client.logout()


def console_main():
    try:
        main()
    except (IOError, AppError), ex:
        sys.stderr.write("%s\n" % ex)
    except imapclient.IMAPClient.Error, ex:
        sys.stderr.write("IMAP Error: %s\n" % ex)
    except KeyboardInterrupt:
        sys.stderr.write('Interrupted\n')


if __name__ == '__main__':
    console_main()
