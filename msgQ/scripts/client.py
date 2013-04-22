#!/usr/bin/env python

import socket
import json
from msgQ import config

_config = config.load()


def send(msg, topic='*', mod='*'):
    recv = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((_config['address'], _config['port']))

        message = dict(msg=msg, topic=topic, mod=mod)
        sock.send(json.dumps(message) + '\n')
        recv = sock.recv(1024)
    finally:
        sock.close()

    return recv
