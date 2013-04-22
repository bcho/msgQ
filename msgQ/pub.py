#coding: utf-8

import logging

from msgQ.queuer import enqueue
from msgQ.commands import get_commands


logger = logging.getLogger('msgQ')


def publish(msg='', topic='*.*'):
    logger.info('New msg received: %s from %s' % (msg, topic))
    for command in get_commands(topic):
        enqueue(command, msg)
