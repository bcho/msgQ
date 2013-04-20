#coding: utf-8

import SocketServer
import json

import msgQ


class _Publisher(object):
    def publish(self, recv):
        mod, topic = str(recv.get('mod', '*')), str(recv.get('topic', '*'))
        msg = recv.get('msg', '')
        msgQ.publish(msg, topic='%s.%s' % (mod, topic))


class MsgHandler(SocketServer.BaseRequestHandler, _Publisher):
    buf_size = 1024

    def handle(self):
        recv = self.request.recv(self.buf_size).strip()

        try:
            self.data = json.loads(recv)
            if not isinstance(self.data, dict):
                self.data = {'msg': recv}
            self.request.send(json.dumps({'result': 0}) + '\n')
        except ValueError as e:
            self.data = {'msg': recv}
            self.request.send(json.dumps({
                'result': 1,
                'err': e[0]
            }) + '\n')
        finally:
            self.request.close()

    def finish(self):
        self.publish(self.data)
