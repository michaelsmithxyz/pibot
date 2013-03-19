#!/usr/bin/env python3

import imp
import logging as l
import os
import os.path

class PluginManager:
    def __init__(self, bundle=None):
        self.handlers = {}
        self.plugins = {}
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
            self.load_plugin(full_name, mod_info)

    def load_plugin(self, name, info):
        mod = imp.load_module(name, *info)
        try:
            modname = mod.NAME
            if modname in self.plugins:
                l.warn("Module", modname, "already loaded. Ignoring duplicate")
            else:
                l.info("Loading Module:", modname)
                plugin = mod.init(self.bundle)
                self.plugins[modname] = plugin
        except Exception as e:
            l.err("Error loading module", name)
            l.err('\t', str(e))

    def initialize(self):
        for plug in self.plugins:
            self.plugins[plug].init()

    def get_plugin(self, name):
        if name in self.plugins:
            return self.plugins[name]
        return None

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
