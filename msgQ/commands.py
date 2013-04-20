#coding: utf-8

'''
msgQ.commands
'''

import logging

from msgQ.config import commands as subscribers
from msgQ.consumer import MsgConsumer


logger = logging.getLogger('msgQ')


def _topic_cmp(key, topic):
    key = [_.strip() for _ in key.split('.')]
    topic = [_.strip() for _ in topic.split('.')]

    if len(key) > len(topic):
        return False
    for i in xrange(len(key)):
        if key[i] != topic[i] and key[i] != '*' and topic[i] != '*':
            return False
    return True


def get_commands(topic):
    logger.debug('Checking commands for %s' % (topic, ))

    commands = []
    for k, c in subscribers.items():
        if _topic_cmp(k, topic):
            if not isinstance(c, MsgConsumer):
                if isinstance(c, str):
                    commands.append(MsgConsumer.from_raw(k, c).consume_raw)
                else:
                    logger.warning('Unsupported command! %s' % k)
            else:
                if c.key == k:
                    commands.append(c.consume)
                else:
                    logger.warning('Unmatched key! %s' % k)
    return commands
