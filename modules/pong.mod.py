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
        self.mgr.add_handler("IRC_PING", self.pong)

    def pong(self, event, args):
        self.bot.send_message(irc.pong(args[2][0]))

def init(bot):
    pl = PongModule(bot)
    return pl
