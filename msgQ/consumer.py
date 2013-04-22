#coding: utf-8

'''
msgQ.consumer
'''


class MsgConsumer(object):
    def __init__(self, key, command=None, raw=False, args=None):
        self.key = key
        self.command = command
        self._is_raw = raw
        self._extra_args = args or ''

    def consume(self, payload):
        '''Adapt this method to handle the message'''
        if self._is_raw:
            return self._consume_raw(payload)
        else:
            raise NotImplementedError

    def _consume_raw(self, payload):
        '''Execute from string.'''
        if not self.command:
            raise AttributeError

        import sh
        c = sh.Command(self.command)(self._extra_args, payload)
        c.wait()
        return c.exit_code

    def __str__(self):
        return '<Consumer %s>' % (self.key)
