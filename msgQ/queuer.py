#coding: utf-8

'''
msgQ.queuer

Provide a job queue.
'''

from redis import Redis
from rq import Queue, Connection


def enqueue(command, msg):
    with Connection(Redis()):
        q = Queue()
        q.enqueue(command, msg)
