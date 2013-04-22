#coding: utf-8

import os
import copy
import logging

from consumer import MsgConsumer


logger = logging.getLogger('msgQ')

MSGQ_ERROR_TOPIC = 'msgQ.error'
MSGQ_GREET_TOPIC = 'msgQ.greeting'
DEFAULT_CONFIG_FILE = 'msgqconf.py'

BUILTIN_COMMANDS = [
    dict(
        topic=MSGQ_ERROR_TOPIC,
        command='notify-send',
        args='--urgency=critical',
        activate=True
    ),
    dict(
        topic=MSGQ_GREET_TOPIC,
        command='notify-send'
    )
]
BUILTIN = {
    'address': '',
    'port': 1024,
    'commands': BUILTIN_COMMANDS
}


def load(filename=DEFAULT_CONFIG_FILE):
    def _load_config_file(filename):
        local = {}
        execfile(filename, {}, local)

        config = local.get('config', {})
        commands = config.pop('commands', [])
        return config, commands

    def _preprocess_commands(commands):
        for c in commands:
            if not isinstance(c['command'], MsgConsumer):
                if isinstance(c['command'], str):
                    c['command'] = MsgConsumer(c['topic'],  c['command'], True,
                                               c.get('args', ''))
                else:
                    logger.warning('Unsupported command type for %s' % c['t'])

    config = copy.deepcopy(BUILTIN)

    if os.path.exists(filename):
        updated_config, updated_commands = _load_config_file(filename)
        config.update(updated_config)
        config['commands'].extend(updated_commands)
    else:
        logger.warning('config file %s does not exist!' % (filename))

    _preprocess_commands(config['commands'])

    return config
