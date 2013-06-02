#!/usr/bin/env python

import events
import plugin


class LoggingModule(plugin.PiPlugin):
    def __init__(self, bot, manager):
        self.name = "mod_logging"
        super().__init__(bot, manager)
        self.conf = self.bot.get_config()
    
    @plugin.hooks([events.READ_MESSAGE, events.WRITE_MESSAGE])
    def log(self, event, args):
        if self.conf.get_value("bot.logconsole").lower() == 'true':
            msg = args[0]
            self.logger.info(msg.rstrip())
