#!/usr/bin/env python3

import events
import logging as l

class CommandManager:
    HOOKS = {}
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_config()
        self.prefix = '!'

    @classmethod
    def hook_command(cls, command, alias=''):
        def _decor(function):
            cls.register(cls, command, function, alias=alias)
            def wrapper(*args, **kwargs):
                function(*args, **kwargs)
            return wrapper
        return _decor
        
    def enable(self):
        p = self.config.get_value("commands.prefix")
        if p is not None:
            self.prefix = p
        else:
            self.prefix = '!'

    def privmsg(self, event, args):
        if not (len(args[2]) > 0 and args[2][0] == self.prefix):
            return
        command = args[2].split(' ')
        if len(command) < 2:
            return
        command = command[1:].lower()
        cargs = ' '.join(args[2].split(' ')[1:])
        source = args[0]
        if args[1] == self.bot.get_nick():
            replyto = source
        else:
            replyto = target
        if command in self.handlers:
            l.info("Handling command:", command)
            self.handlers[command](command, cargs, source, replyto)

    def register(self, command, handler):
        command = command.lower()
        if command in self.handlers:
            return None
        self.handlers[command] = handlers
        return command

    def unregister(self, command):
        if command in self.handlers:
            del self.handlers[command]
