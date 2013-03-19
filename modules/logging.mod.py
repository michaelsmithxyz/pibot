#!/usr/bin/env python

import events
import irc
import logging as l

NAME = 'mod_logging'

class LoggingModule:
    def __init__(self, bot):
        self.bot = bot
        self.mgr = self.bot.get_plugin_manager()
        self.conf = self.bot.get_config()
    
    def init(self):
        if self.conf.get_value("bot.logconsole").lower() == 'true':
            l.info("Logging enabled")
            self.mgr.add_handler(events.READ_MESSAGE, self.log)
            self.mgr.add_handler(events.WRITE_MESSAGE, self.log)

    def log(self, event, args):
        msg = args[0]
        l.info(msg.rstrip())

def init(bot):
    pl = LoggingModule(bot)
    return pl
