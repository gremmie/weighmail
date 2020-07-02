=========
weighmail
=========
An application to label your Gmail messages according to size
-------------------------------------------------------------

:Author: Brian Neal <bgneal@gmail.com>
:Version: 0.1.0
:Date: May 20, 2012
:Home Page: https://bitbucket.org/bgneal/weighmail/
:License: New BSD License (see LICENSE.txt)
:Support: https://bitbucket.org/bgneal/weighmail/issues


Overview
--------

``weighmail`` is a program that analyzes your Gmail and applies labels to your
messages according to their size. This is useful if you are close to reaching
your quota as it allows you to quickly identify large messages. You have
complete control over the rules used to create the labels.


Installation
------------

``weighmail`` can be installed using Pip_::

   $ pip install weighmail

Alternatively you can download a tarball and install with::

   $ python setup.py install

``weighmail`` depends on the IMAPClient_ library. This library is automatically
installed if you use Pip_.

Gmail Notes
-----------

In case it isn't clear, ``weighmail`` works with Gmail_. You must have a Gmail
account with `IMAP support turned on`_. Please go into your settings and verify
IMAP support is turned on before proceeding.

If you are using `two-step verification`_ on your Gmail account (**and you
really should be**), you `need to generate an application specific password`_
for ``weighmail`` to use. In this case you will use an application specific
password instead of your normal password when running ``weighmail``.


Usage
-----

``weighmail`` can accept options from a configuration file and/or the
command-line. Command-line arguments always take precedence over options found
in the configuration file.

Command-Line Arguments
~~~~~~~~~~~~~~~~~~~~~~

``weighmail`` takes a fair number of arguments on the command-line. Most of
these can be omitted however, as they all have sensible defaults. In fact, the
simplest way to run ``weighmail`` is as follows::

   $ weighmail --labels big:1MB-5MB huge:5MB-10MB enormous:10MB-

This example demonstrates:

* A *big* label will be applied to messages between 1 and 5 Megabytes
* A *huge* label will be applied to messages between 5 and 10 Megabytes
* An *enormous* label will be applied to messages 10 MB and bigger
* Since no ``user`` or ``password`` options were supplied on the command-line,
  ``weighmail`` will interactively prompt for them. Neither will be echoed out
  for privacy reasons.

To see a list of all command-line options::

   $ weighmail --help

Some notes on the options follows.

* The ``--config`` option is used to specify a configuration file that
  ``weighmail`` will read for options. Any options supplied on the command-line
  will override any options from this file. In particular, if you specify any
  label rules on the command-line, all label rules in the configuration file
  will be ignored.
* The ``--folder`` option can be used to specify which Gmail label to search for
  messages. This defaults to your *All Mail* label.
* The ``--user`` and ``--password`` options are used to specify which Gmail
  account to log into. If these are not supplied, and also omitted from a config
  file (or if no config file is being used), ``weighmail`` will prompt you for
  these options.
* The ``--labels`` argument is how you specify the rules for labeling your
  messages. See the sub-section below for more detail on this syntax.
* The ``--host``, ``--port``, and ``--nossl`` arguments are for advanced use
  only, and may in fact not work. The defaults should work for most people, and
  will connect you to ``imap.gmail.com`` port 993 using SSL.

The --labels argument syntax
++++++++++++++++++++++++++++

To specify label rules on the command-line, use the following syntax::

   $ weighmail --labels name:min-max [name:min-max] ...

Where:

* *name* is the name of the label. Note that Gmail labels cannot have spaces in
  them.
* *min* and *max* specify the message size range in bytes. Either one, but not
  both, may be omitted (but the dash must remain). You may use the suffixes
  ``KB``, ``MB``, or ``GB`` to indicate kilobytes, Megabytes, or Gigabytes,
  respectively.

Another example::

   $ weighmail --labels normal:-2MB big:2MB-7MB huge:7MB-
 
In all these examples the label ranges do not overlap. This does not have to be
the case; overlapping ranges may be defined if desired.


Configuration File
~~~~~~~~~~~~~~~~~~

If you specify the ``--config=filename`` option on the command-line,
``weighmail`` will parse this file for options. Please see the included
`sample-weighmail.ini` file for the syntax and option descriptions.

Again, note that command-line arguments take precedence over options found in
the configuration file. If you specify *any* label rules on the command-line,
*all* label rules in the configuration file are ignored.


Thanks
~~~~~~

A big thank-you to Menno Smits, the author of the IMAPClient_ library. This
application would have been considerably more complicated if the awesome
IMAPClient library did not exist.


.. _Pip: http://pypi.python.org/pypi/pip
.. _Gmail: http://mail.google.com/
.. _IMAP support turned on: http://support.google.com/mail/bin/answer.py?hl=en&answer=77695
.. _two-step verification: http://support.google.com/accounts/bin/answer.py?hl=en&answer=180744
.. _need to generate an application specific password: http://support.google.com/accounts/bin/answer.py?hl=en&answer=185833&topic=1056283&ctx=topic
.. _IMAPClient: http://pypi.python.org/pypi/IMAPClient/
