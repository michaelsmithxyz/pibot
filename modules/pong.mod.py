#!/usr/bin/env python

class PongPlugin:
    def __init__(self, bot, irc, l, events, mgr):
        self.irc = irc
        self.mgr = mgr
        self.bot = bot
        self.events = events
        self.l = l
    
    def init(self):
        self.mgr.add_handler(self.events.READ_MESSAGE, self.pong)

    def pong(self, event, args):
        msg = self.irc.parse_message(args[0])
        if msg[0] == 'PING':
            self.l.info("Pong", msg[1])
            self.bot.send_message(self.irc.pong(msg[1]))

def init(bundle):
    pl = PongPlugin(bundle[0], bundle[1], bundle[2], bundle[3], bundle[5])
    pl.init()
    return pl
