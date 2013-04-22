#coding: utf-8


from .logger import setup_logger
logger = setup_logger('msgQ')

from .pub import publish


__all__ = ['publish']
