"""weighmail - Copyright (C) 2012 by Brian Neal

Released under the New BSD license, see LICENSE.txt.

"""
from setuptools import setup, find_packages
from os.path import join, dirname

import weighmail

setup(
    name='weighmail',
    version=weighmail.__version__,
    author='Brian Neal',
    author_email='bgneal@gmail.com',
    packages=find_packages(),
    url='https://bitbucket.org/bgneal/weighmail/',
    license='BSD',
    description='Labels your Gmail messages according to size.',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_points={
        'console_scripts': ['weighmail = weighmail.main:console_main'],
    },
    install_requires=[
        'IMAPClient >= 0.9',
        'distribute',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Communications :: Email',
        'Topic :: Communications :: Email :: Post-Office :: IMAP',
    ],
)
