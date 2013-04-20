#coding: utf-8

import SocketServer
import json
import threading


class _MsgHandler(SocketServer.BaseRequestHandler):
    buf_size = 1024

    def handle(self):
        recv = self.request.rect(self.buf_size).strip()
        try:
            self.data = json.loads(recv)
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
        raise NotImplementedError


class MsgServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True

    def __init__(self, server_addr, RequestHandlerClass=_MsgHandler,
                 bind_and_activate=True):
        SocketServer.TCPServer.__init__(self, server_addr, RequestHandlerClass,
                                        bind_and_activate)


def create_server(host, port):
    '''Create a MsgServer and SocketServer.server_thread instance.
    To use them, try:

        server, thread = create_server('', 1024)
        try:
            server.serve_forever()
        except KeyboardIntrrupt:
            server.shutdown()
    '''
    server = MsgServer((host, port))
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True

    return server, server_thread
