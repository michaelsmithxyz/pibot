#!/usr/bin/env python

import events
import irc
import logging as l

NAME = 'mod_pong'

class PongModule:
    def __init__(self, bot):
        self.bot = bot
        self.mgr = bot.get_plugin_manager()
    
    def init(self):
        self.mgr.add_handler(events.READ_MESSAGE, self.pong)

    def pong(self, event, args):
        msg = irc.parse_message(args[0])
        if msg[0] == 'PING':
            self.bot.send_message(irc.pong(msg[1]))

def init(bot):
    pl = PongModule(bot)
    return pl
