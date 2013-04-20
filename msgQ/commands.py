#coding: utf-8

'''
msgQ.commands
'''

import logging
import os

logger = logging.getLogger('msgQ')


def foo(msg):
    return os.system('notify-send %s' % msg)


def get_commands(topic):
    logger.debug('Checking commands for %s' % (topic, ))
    return ['msgQ.commands.foo']
