#!/usr/bin/env python

import events
import irc
import logging as l
from plugin import PiPlugin, PluginManager

class LoggingModule(PiPlugin):
    def __init__(self, bot, manager):
        super().__init__(bot, manager)
        self.conf = bot.get_config()
        self.name = "logging"
    
    #def enable(self):
    #    if self.conf.get_value("bot.logconsole").lower() == 'true':
    #        self.manager.add_handler(events.READ_MESSAGE, self.log)
    #        self.manager.add_handler(events.WRITE_MESSAGE, self.log)

    @PluginManager.hook_event(events.READ_MESSAGE)
    def log(self, event, args):
        msg = args[0]
        l.info(msg.rstrip())
