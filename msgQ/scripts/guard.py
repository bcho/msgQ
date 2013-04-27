#coding: utf-8

from os import path
import logging

from msgQ.server import create_server
from msgQ.cli import get_arguments
from msgQ import config as msgq_config


logger = logging.getLogger('msgQ')


def serve(config):
    server, thread = create_server(config['address'], config['port'])
    try:
        logger.info('Server start listening at %(address)s:%(port)d...'
                    'don\'t forget to run rqworker...' % (config))
        server.serve_forever()
    finally:
        server.shutdown()


def main():
    arguments = get_arguments()
    if '-c' in arguments and arguments.get('FILE'):
        config = msgq_config.load(path.abspath(arguments['FILE']))
    else:
        config = msgq_config.load()
    serve(config)


if __name__ == '__main__':
    main()
