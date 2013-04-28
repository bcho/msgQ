#!/usr/bin/env python
#coding: utf-8


import SocketServer
import threading
import json
import logging

import msgQ
from msgQ import queue, commands


logger = logging.getLogger(msgQ.__name__)


class _PublisherMixin(object):
    def publish(self, recv):
        mod, topic = str(recv.get('mod', '')), str(recv.get('topic', '*'))
        msg = recv.get('msg', '')

        for command in commands.get(mod, topic,
                                    self.server.config['commands']):
            queue.enqueue(command, msg, mod, topic)


class MsgHandler(SocketServer.BaseRequestHandler, _PublisherMixin):
    buf_size = 1024

    def handle(self):
        recv = self.request.recv(self.buf_size).strip()

        try:
            self.data = json.loads(recv)
            if not isinstance(self.data, dict):
                self.data = {'msg': recv}
            self.request.send(json.dumps({'result': 0}) + '\n')
        except ValueError as e:
            self.data = {
                'msg': 'Received raw message %s' % recv,
                'topic': 'error',
                'mod': 'msgQ'
            }
            self.request.send(json.dumps({
                'result': 1,
                'err': e[0]
            }) + '\n')
        finally:
            self.request.close()

    def finish(self):
        self.publish(self.data)


class MsgServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    '''TCP Server'''
    allow_reuse_address = True

    def __init__(self, server_addr, config, RequestHandlerClass=MsgHandler,
                 bind_and_activate=True):
        SocketServer.TCPServer.__init__(self, server_addr, RequestHandlerClass,
                                        bind_and_activate)
        self.config = config


def _build_treading_server(host, port, config):
    server = MsgServer((host, port), config)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    return server, server_thread


def build(config):
    host, port = config['host'], config['port']
    server, thread_server = _build_treading_server(host, port, config)
    return server
