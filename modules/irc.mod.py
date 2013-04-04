#!/usr/bin/env python3

import events
import irc
import logging as l

NAME = 'mod_irc'

class IRCModule:
    def __init__(self, bot):
        self.bot = bot
        self.mgr = self.bot.get_plugin_manager()

    def init(self):
        self.mgr.add_handler(events.READ_MESSAGE, self.dispatch)
        self.mgr.add_handler("IRC_PRIVMSG", self.d_privmsg)

    def dispatch(self, event, args):
        msg = args[0].rstrip()
        parts = irc.parse_message(msg)
        evt = "IRC_%s" % parts[1]
        self.mgr.handle_event(evt, parts)

    def d_privmsg(self, event, args):
        source = irc.parse_nick(args[0])[0]
        target = args[2][0]
        msg = args[2][1]
        self.mgr.handle_event(events.PRIVMSG, [source, target, msg])

def init(bot):
    ir = IRCModule(bot)
    return ir
