#!/usr/bin/env python
#coding: utf-8

import logging

import msgQ


logger = logging.getLogger(msgQ.__name__)


def _mod_cmp(key, mod):
    if not key or not mod:
        return True
    return key == mod


def _topic_cmp(key, topic):
    key = [_.strip() for _ in key.split('.')]
    topic = [_.strip() for _ in topic.split('.')]

    if len(key) > len(topic):
        return False
    for i in xrange(len(key)):
        if key[i] != topic[i] and key[i] != '*' and topic[i] != '*':
            return False
    return True


def get(mod, topic, subscribers):
    logger.debug('Got message from %s.%s' % (mod, topic))
    commands = []
    for sub in subscribers:
        if sub.get('activate', True) and _mod_cmp(sub.get('mod'), mod) and\
                _topic_cmp(sub.get('topic', '*'), topic):
            commands.append(sub['command'].consume)
    return commands
