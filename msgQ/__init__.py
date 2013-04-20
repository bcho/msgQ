#coding: utf-8

from .logger import setup_logger
from .queuer import enqueue
from .commands import get_commands


logger = setup_logger('msgQ')


def publish(msg='', topic='*.*'):
    logger.info('New msg received: %s from %s' % (msg, topic))
    for command in get_commands(topic):
        enqueue(command, msg)
