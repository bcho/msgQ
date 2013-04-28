#!/usr/bin/env python
#coding: utf-8

import logging

DEFAULT_FORMAT = '''%(levelname)s - %(message)s'''
DEFAULT_LEVEL = logging.DEBUG


def logging_factory(handler, level=None, format=None):
    level = level or DEFAULT_LEVEL
    format = format or DEFAULT_FORMAT
    handler.setLevel(level)
    if getattr(handler, 'setFormatter', None):
        handler.setFormatter(logging.Formatter(format))
    return handler


def setup(name, level=None, format=None, handler=None):
    logger = logging.getLogger(name)
    logger = logging_factory(logger, level, format)

    for i in handler or [logging.StreamHandler()]:
        logger.addHandler(logging_factory(i, level, format))

    return logger
