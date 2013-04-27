#coding: utf-8

'''
msgQ.cli

Provide command line interface.
'''

from docopt import docopt

NAME = 'msgq'
VERSION = '0.0.1'


opt = '''%(name)sctl

Usage:
    %(name)sctl [-c FILE]

Options:
    -h --help   Show this screen.
    --version   Show version.
    -c          Set configuration file

''' % {
    'name': NAME
}


def get_arguments():
    return docopt(opt, version=VERSION)
