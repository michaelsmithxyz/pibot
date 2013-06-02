#!/usr/bin/env python

import events
import irc
import plugin

class ChannelsModule(plugin.PiPlugin):
    def __init__(self, bot, manager):
        self.name = "mod_channels"
        super().__init__(bot, manager)
        self.channels = {}
        self.conf = self.bot.get_config()

    @plugin.hooks(events.POST_CONNECT)
    def connect_handler(self, event, args):
        if self.conf.get_value("bot.channel"):
            channel = self.conf.get_value("bot.channel")
            self.bot.send_message(irc.join(channel))
            self.channels[channel] = []

    @plugin.hooks(events.EXIT)
    def exit_handler(self, event, args):
        for chan in self.channels:
            self.bot.send_message(irc.part(chan))

    @plugin.hooks("IRC_353")
    def namerpl_handler(self, event, args):
        names = irc.parse_names(args)
        if names[0] in self.channels:
            self.channels[names[0]] = [irc.raw_nick(x) for x in names[1]]

    @plugin.hooks("IRC_JOIN")
    def join_handler(self, event, args):
        nick = irc.raw_nick(irc.parse_nick(args[0]))
        chan = args[2][0]
        if chan in self.channels:
            if nick not in self.channels[chan]:
                self.channels[chan].append(nick)
        self.manager.handle_event(events.JOIN, [nick, chan])

    @plugin.hooks("IRC_PART")
    def part_handler(self, event, args):
        nick = irc.raw_nick(irc.parse_nick(args[0])[0])
        chan = args[2][0]
        if chan in self.channels:
            if nick in self.channels[chan]:
                self.channels[chan].remove(nick)
        self.manager.handle_event(events.PART, [nick, chan])
