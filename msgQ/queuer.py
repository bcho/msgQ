#coding: utf-8

'''
msgQ.queuer

Provide a job queue.
'''

import logging

from redis import Redis
from rq import Queue, Connection


logger = logging.getLogger('msgQ')


def enqueue(command, msg):
    with Connection(Redis()):
        q = Queue()
        q.enqueue(command, msg)
