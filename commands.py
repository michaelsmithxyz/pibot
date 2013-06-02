#!/usr/bin/env python3

import events
import logging

class CommandManager(object):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_config()
        self.mgr = self.bot.get_plugin_manager()
        self.logger = logging.getLogger()
        self.handlers = {}
        p = self.config.get_value("commands.prefix")
        if p is not None:
            self.prefix = p
        else:
            self.prefix = '!'
        self.mgr.add_handler(events.PRIVMSG, self.privmsg)

    def privmsg(self, event, args):
        if not (len(args[2]) > 0 and args[2][0] == self.prefix):
            return
        command = args[2].split(' ')[0]
        if len(command) < 2:
            return
        command = command[1:].lower()
        cargs = ' '.join(args[2].split(' ')[1:])
        source = args[0]
        target = args[1]
        if args[1] == self.bot.get_nick():
            replyto = source
        else:
            replyto = target
        self.handle_command(command, cargs, source, replyto)

    def handle_command(self, command, args, source, replyto):
        if command in self.handlers:
            self.logger.debug("Handling command:", command)
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
