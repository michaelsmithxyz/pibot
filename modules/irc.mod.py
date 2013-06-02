#!/usr/bin/env python3

import events
import irc
import logging as l
import plugin

class IRCModule(plugin.PiPlugin):
    def __init__(self, bot, manager):
        self.name = "mod_irc"
        super().__init__(bot, manager)

    @plugin.hooks(events.READ_MESSAGE)
    def dispatch(self, event, args):
        msg = args[0].rstrip()
        parts = irc.parse_message(msg)
        evt = "IRC_%s" % parts[1]
        self.manager.handle_event(evt, parts)

    @plugin.hooks("IRC_PRIVMSG")
    def d_privmsg(self, event, args):
        source = irc.parse_nick(args[0])[0]
        target = args[2][0]
        msg = args[2][1]
        self.manager.handle_event(events.PRIVMSG, [source, target, msg])
