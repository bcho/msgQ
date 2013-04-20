#coding: utf-8

'''
msgQ.consumer
'''


class MsgConsumer(object):
    def __init__(self, key, command=None):
        self.key = key
        self.command = command

    def consume(self, payload):
        '''Adapt this method to handle the message'''
        raise NotImplementedError

    def consume_raw(self, payload):
        '''Execute from string.'''
        if not self._is_raw and self.command:
            raise AttributeError

        import sh
        c = sh.Command(self.command)(payload)
        c.wait()
        return c.exit_code

    @staticmethod
    def from_raw(key, command):
        c = MsgConsumer(key, command)
        c._is_raw = True
        return c
