#!/usr/bin/env python
#coding: utf-8

import sys
import socket
import json
from docopt import docopt

import msgQ
from msgQ.config import BUILTIN_CONFIG


__NAME__ = 'msgq'

opt = '''%(name)s

Usage:
    %(name)s <message> [-a|--host <host>] [-p|--port <port>] [-m|--mod <mod>] \
[-t|--topic <topic>]

    -a --host   specify host
    -p --port   specify port
    -m --mod    specify mod
    -t --topic  specify topic
    -h --help   show this screen
    -v --version   show version

''' % {
    'name': __NAME__
}


def send(host, port, msg, mod='*', topic='*'):
    recv = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        message = dict(msg=msg, mod=mod, topic=topic)
        sock.send(json.dumps(message) + '\n')
        recv = sock.recv(1024)
    except socket.error as e:
        print e
        sys.exit(1)
    finally:
        sock.close()

    return recv


def main():
    args = docopt(opt, version=msgQ.__version__)
    host, port = BUILTIN_CONFIG['host'], BUILTIN_CONFIG['port']
    host = args['<host>'] if args['--host'] else BUILTIN_CONFIG['host']
    port = int(args['<port>'] if args['--port'] else BUILTIN_CONFIG['port'])
    mod = args['<mod>'] if args['--mod'] else 'msgq'
    topic = args['<topic>'] if args['--topic'] else 'sender.*'
    msg = args['<message>']

    send(host, port, msg, mod, topic)


if __name__ == '__main__':
    main()
