#!/usr/bin/env python
#coding: utf-8

import os
import copy
import logging

import msgQ
from msgQ.consumer import Consumer


logger = logging.getLogger(msgQ.__name__)

MSGQ_MOD = 'msgQ'
MSGQ_ERROR_TOPIC = 'error'
MSGQ_GREET_TOPIC = 'greeting'
DEFAULT_CONFIG_PATH = '~/.config/msgq'
DEFAULT_CONFIG_FILE = 'msgqconf.py'
CONFIG_PATH = [os.path.join(DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_FILE),
               DEFAULT_CONFIG_FILE]

BUILTIN_COMMANDS = [
    dict(
        mod=MSGQ_MOD,
        topic=MSGQ_ERROR_TOPIC,
        command='notify-send',
        extra_args='--urgency=critical',
        activate=True
    ),
    dict(
        mod=MSGQ_MOD,
        topic=MSGQ_GREET_TOPIC,
        command='notify-send'
    )
]
BUILTIN_CONFIG = {
    'host': '127.0.0.1',
    'port': 1024,
    'commands': BUILTIN_COMMANDS
}


def build(setting_file=None):
    def _load_config_from_file(fname):
        fname = os.path.abspath(os.path.expanduser(fname))
        if not os.path.exists(fname):
            logger.warning('Config file %s does not exist!' % (setting_file))
            return None, None

        local = {}
        execfile(fname, {}, local)

        config = local.get('config', {})
        commands = config.pop('commands', [])
        return config, commands

    def _preprocess_commands(commands):
        for c in commands:
            if not isinstance(c['command'], Consumer):
                if isinstance(c['command'], str):
                    c['command'] = Consumer(raw=True, **c)

    config = copy.deepcopy(BUILTIN_CONFIG)
    search_path = CONFIG_PATH

    if setting_file:
        search_path.append(setting_file)
    search_path = list(set(search_path))
    for config_path in search_path:
        fconfig, fcommands = _load_config_from_file(config_path)
        if fconfig:
            config.update(fconfig)
        if fcommands:
            config['commands'].extend(fcommands)

    _preprocess_commands(config['commands'])

    return config
