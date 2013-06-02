#!/usr/bin/env python3

import logging

class Config(object):
    def __init__(self, bot):
        self.registry = {}
        self.bot = bot
        self.logger = logging.getLogger()

    def set_value(self, key, value):
        self.registry[key] = value

    def get_value(self, key):
        if key in self.registry:
            return self.registry[key]
        return None

    def del_value(self, key):
        if key in self.registry:
            del self.registry[key]

    def read(self, path):
        try:
            self.logger.info("Reading configuration %s", path)
            conf = open(path, 'r')
            for line in conf:
                line = line.strip()
                if len(line) > 0:
                    if line[0] == '#':
                        continue
                    parts = line.split('=')
                    self.registry[parts[0].strip()] = parts[1].strip()
            conf.close()
        except Exception as e:
            self.logger.error("Error reading configuration")
            l.err("\t", str(e))
            self.bot._quit()

    def write(self, path):
        try:
            self.logger.info("Writing configuration", path)
            conf = open(path, 'w')
            for key, value in self.registry.items():
                conf.write("%s = %s\n" %(key, value))
            conf.close()
        except Exception as e:
            self.logger.error("Error writing configuration")
            self.logger.error("\t", str(e))
        
    def check(self, required):
        ret = []
        for option in required:
            if option not in self.registry:
                ret.append(option)
        return ret
