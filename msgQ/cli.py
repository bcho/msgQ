#!/usr/bin/env python
#coding: utf-8

import sys
from docopt import docopt

import msgQ
from msgQ import config, server, logger


opt = '''%(name)sd

Usage:
    %(name)sd serve [--host=<HOST>] [--port=<PORT>] [--config=<FILE>]

Options:
    --config=<FILE> Specify configuration file.
    --host=<HOST>   Specify host.
    --port=<PORT>   Specify port.
    -h --help       Show this screen.
    --version       Show version.

''' % {
    'name': msgQ.__name__.lower(),
}


def main():
    log = logger.setup(msgQ.__name__)

    arguments, command = docopt(opt, version=msgQ.__version__), 'help'
    if len(sys.argv) > 1:
        command = sys.argv[1]

    if command == 'serve':
        _config = config.build(arguments.get('--config', None))

        if arguments['--host']:
            _config['host'] = arguments['--host']
        if arguments['--port']:
            _config['port'] = int(arguments['--port'])

        _server = server.build(_config)
        log.info('Start listening on %(host)s:%(port)d '
                 'don\'t forget to enable rqworker' % _config)
        _server.serve_forever()
    elif command == 'help':
        print opt


if __name__ == '__main__':
    main()
