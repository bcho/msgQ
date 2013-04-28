#!/usr/bin/env python
#coding: utf-8


class Consumer(object):
    def __init__(self, mod=None, topic=None, command=None, raw=False,
                 extra_args=None, *args, **kwargs):
        self.key = topic or '*'
        if mod:
            self.key = '%s.%s' % (mod, self.key)
        self.command = command
        self._raw = raw
        self._extra_args = extra_args or ''

    def consume(self, payload):
        '''Adapt this method to handle the message'''
        if self._raw:
            return self._consume_raw(payload)
        else:
            raise NotImplementedError

    def _consume_raw(self, payload):
        '''Execute from string.'''
        if not self.command:
            raise AttributeError

        import sh
        c = sh.Command(self.command)(payload, self._extra_args)
        c.wait()
        return c.exit_code

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<Consumer %s>' % (self.key)
