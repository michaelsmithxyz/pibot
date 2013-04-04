#!/usr/bin/env python3

class CommandManager:
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.get_config()
        p = self.config.get_value("commands.prefix")
        if p is not None:
            self.prefix = p
        else:
            self.prefix = '!'
