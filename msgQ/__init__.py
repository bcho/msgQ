#coding: utf-8

from .queuer import enqueue
from .commands import get_commands


def publish(msg='', topic='*.*'):
    for command in get_commands(topic):
        enqueue(command, msg)
