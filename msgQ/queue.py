#!/usr/bin/env python
#coding: utf-8

from redis import Redis
from rq import Queue, Connection
import logging

import msgQ


logger = logging.getLogger(msgQ.__name__)


def enqueue(command, msg, mod='', topic='*'):
    logger.debug('New job from %s.%s enqueued' % (mod, topic))
    with Connection(Redis()):
        q = Queue()
        q.enqueue(command, msg)
