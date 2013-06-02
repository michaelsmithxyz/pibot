#!/usr/bin/env python

import events
import irc
import plugin

class PongModule(plugin.PiPlugin):
    def __init__(self, bot, manager):
        self.name = "mod_pong"
        super().__init__(bot, manager)

    @plugin.hooks("IRC_PING")
    def pong(self, event, args):
        self.bot.send_message(irc.pong(args[2][0]))
