#!/usr/bin/env python3

import imp
import logging as l
import os
import os.path

class PluginManager:
    def __init__(self, bundle=()):
        self.handlers = {}
        self.plugins = []
        bundle = bundle + (self,)
        self.bundle = bundle

    def load(self, path):
        path = os.path.abspath(path)
        files = os.listdir(path)
        for fle in files:
            name = os.path.basename(fle)
            if not name.endswith('.mod.py'):
                continue
            mod_name = name.split('.mod.py')[0]
            full_name = mod_name + '.mod'
            mod_info = imp.find_module(full_name, [path])
            l.info("Loading plugin", full_name)
            self.load_plugin(full_name, mod_info)

    def load_plugin(self, name, info):
        mod = imp.load_module(name, *info)
        try:
            self.plugins.append(mod.init(self.bundle))
        except Exception as e:
            l.err(str(e))
            l.warn("Error loading module", name)

    def handle_event(self, event, args):
        for handle in self.handlers:
            if event in self.handlers[handle]:
                handle(event, args)

    def add_handler(self, event, handler):
        if handler in self.handlers:
            self.handlers[handler].append(event)
        else:
            self.handlers[handler] = [event]
    
    def remove_handler(self, event, handler):
        if handler in self.handlers:
            self.handlers[handler].remove(event)

    def remove_all(self, event, handler):
        if handler in self.handlers:
            del self.handlers[handler]
