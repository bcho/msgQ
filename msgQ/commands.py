#coding: utf-8

'''
msgQ.commands
'''

import logging

from msgQ import config


logger = logging.getLogger('msgQ')
subscribers = config.load().get('commands', [])


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
    for sub in subscribers:
        if sub.get('activate', True) and _topic_cmp(sub['topic'], topic):
            commands.append(sub['command'].consume)
    return commands
