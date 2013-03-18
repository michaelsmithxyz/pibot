#!/usr/bin/env python

class LoggingPlugin:
    def __init__(self, bot, irc, l, events, args, mgr):
        self.irc = irc
        self.mgr = mgr
        self.bot = bot
        self.events = events
        self.l = l
    
    def init(self):
        self.mgr.add_handler(self.events.READ_MESSAGE, self.log)
        self.mgr.add_handler(self.events.WRITE_MESSAGE, self.log)

    def log(self, event, args):
        msg = args[0]
        self.l.info(msg.rstrip())

def init(bundle):
    pl = LoggingPlugin(bundle[0], bundle[1], bundle[2], bundle[3], bundle[4], bundle[5])
    pl.init()
    return pl
