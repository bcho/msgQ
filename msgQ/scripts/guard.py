#coding: utf-8

import os
import logging

import daemon
from msgQ.server import create_server


logger = logging.getLogger('msgQ')


def serve():
    server, thread = create_server('', 1234)
    try:
        logger.info('Server started... don\'t forget to run rqworker...')
        server.serve_forever()
    finally:
        server.shutdown()


def main():
    if os.getuid() == 0:
        with daemon.DaemonContext():
            main()
    else:
        print 'This script must run with root privilege.'


if __name__ == '__main__':
    main()
