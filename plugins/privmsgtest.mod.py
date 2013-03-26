#!/usr/bin/env python

import events
import irc
import logging as l

NAME = 'privmsgtest'

class PrivmsgTest:
    def __init__(self, bot):
        self.bot = bot
        self.mgr = self.bot.get_plugin_manager()
    
    def init(self):
        self.mgr.add_handler("IRC_PRIVMSG", self.handle)

    def handle(self, event, args):
        l.info("Logging PRIVMSG:", args)

def init(bot):
    pl = PrivmsgTest(bot)
    return pl
