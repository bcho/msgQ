#coding: utf-8

'''
TCP socket server suites

Get a server:

    create_server(hostname, port)
'''

import SocketServer
import threading

from handler import MsgHandler


class MsgServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    '''TCP Server'''
    allow_reuse_address = True

    def __init__(self, server_addr, RequestHandlerClass=MsgHandler,
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
