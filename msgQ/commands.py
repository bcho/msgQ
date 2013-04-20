#coding: utf-8

'''
msgQ.commands
'''

import os


def foo(msg):
    return os.system('notify-send %s' % msg)


def get_commands(topic):
    return ['msgQ.commands.foo']
