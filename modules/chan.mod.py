#!/usr/bin/env python

import events
import irc
import logging as l

NAME = 'mod_channels'

class ChannelsModule:
    def __init__(self, bot):
        self.bot = bot
        self.mgr = self.bot.get_plugin_manager()
        self.channels = {}
        self.conf = self.bot.get_config()

    def init(self):
        self.mgr.add_handler(events.POST_CONNECT, self.connect_handler)
        self.mgr.add_handler(events.EXIT, self.exit_handler)
        self.mgr.add_handler("IRC_353", self.namerpl_handler)
        self.mgr.add_handler("IRC_JOIN", self.join_handler)
        self.mgr.add_handler("IRC_PART", self.part_handler)

    def connect_handler(self, event, args):
        if self.conf.get_value("bot.channel"):
            channel = self.conf.get_value("bot.channel")
            self.bot.send_message(irc.join(channel))
            self.channels[channel] = []

    def exit_handler(self, event, args):
        for chan in self.channels:
            self.bot.send_message(irc.part(chan))

    def namerpl_handler(self, event, args):
        names = irc.parse_names(args)
        if names[0] in self.channels:
            self.channels[names[0]] = [irc.raw_nick(x) for x in names[1]]

    def join_handler(self, events, args):
        nick = irc.raw_nick(irc.parse_nick(args[0]))
        chan = args[2][0]
        if chan in self.channels:
            if nick not in self.channels[chan]:
                self.channels[chan].append(nick)
        self.mgr.handle_event(events.JOIN, [nick, chan])

    def part_handler(self, events, args):
        nick = irc.raw_nick(irc.parse_nick(args[0])[0])
        chan = args[2][0]
        if chan in self.channels:
            if nick in self.channels[chan]:
                self.channels[chan].remove(nick)
        self.mgr.handle_event(events.PART, [nick, chan])

def init(bot):
    pl = ChannelsModule(bot)
    return pl
