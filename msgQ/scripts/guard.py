#coding: utf-8

import os
import logging
import daemon

from msgQ.server import create_server
from msgQ import config


logger = logging.getLogger('msgQ')
_config = config.load()


def serve():
    server, thread = create_server(_config['address'], _config['port'])
    try:
        logger.info('Server start listening at %(address)s:%(port)d...'
                    'don\'t forget to run rqworker...' % (_config))
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
