#!/usr/bin/env python

import events
import irc
import logging as l

NAME = 'mod_channels'

class ChannelsModule:
    def __init__(self, bot):
        self.bot = bot
        self.mgr = self.bot.get_plugin_manager()
        self.channels = []
        self.conf = self.bot.get_config()

    def init(self):
        self.mgr.add_handler(events.POST_CONNECT, self.connect_handler)
        self.mgr.add_handler(events.EXIT, self.exit_handler)

    def connect_handler(self, event, args):
        if self.conf.get_value("bot.channel"):
            channel = self.conf.get_value("bot.channel")
            self.bot.send_message(irc.join(channel))
            self.channels.append(channel)

    def exit_handler(self, event, args):
        for chan in self.channels:
            self.bot.send_message(irc.part(chan))

def init(bot):
    pl = ChannelsModule(bot)
    return pl
