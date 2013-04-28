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
DEFAULT_CONFIG_FILE = 'msgqconf.py'

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

    setting_file = setting_file or DEFAULT_CONFIG_FILE
    setting_file = os.path.abspath(os.path.expanduser(setting_file))
    if os.path.exists(setting_file):
        fconfig, fcommands = _load_config_from_file(setting_file)
        config.update(fconfig)
        config['commands'].extend(fcommands)
    else:
        logger.warning('Config file %s does not exist!' % (setting_file))

    _preprocess_commands(config['commands'])

    return config
