#!/usr/bin/env python3

import imp
import inspect
import logging as l
import os
import os.path


class PluginError(Exception):
    pass


class PluginManager:
    def __init__(self, bundle=None):
        self.handlers = {}
        self.plugins = {}
        self.bundle = bundle

    def load(self, path):
        path = os.path.abspath(path)
        if not os.path.exists(path):
            l.warn("Skipping modules from", path)
            return
        l.info("Loading modules from", path)
        files = os.listdir(path)
        for fle in files:
            name = os.path.basename(fle)
            if not name.endswith('.mod.py'):
                continue
            mod_name = name.split('.mod.py')[0]
            full_name = mod_name + '.mod'
            mod_info = imp.find_module(full_name, [path])
            self._load_plugin(full_name, mod_info)

    def _load_plugin(self, name, info):
        mod = imp.load_module(name, *info)
        plugins = self._find_plugins(mod, PiPlugin)
        try:
            for plugin in plugins:
                instance = plugin(self.bot, self)
                if not hasattr(instance, 'name'):
                    raise PluginError("Plugin %s does not have a name" %(instance))
                self.plugins.append(instance)
                l.info("Loaded plugin", instance.name)
        except Exception as e:
            l.err("Error loading module", name)
            l.err('\t', str(e))

    def _find_plugins(self, module, base):
        return [cls for name, cls in inspect.getmembers(module) if
            inspect.isclass(cls) and issubclass(cls, base)
            and cls is not base]

    def initialize(self):
        for plug in self.plugins:
            l.info("Initalizing Module:", plug)
            self.plugins[plug].init()

    def unload_plugin(self, name):
        if name in self.plugins:
            plug = self.plugins[name]
            if hasattr(plug, "unload"):
                plug.unload()

    def unload_all(self):
        for plug in self.plugins:
            self.unload_plugin(plug)

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


class PiPlugin:
    def __init__(self, bot, manager):
        self.bot = bot
        self.manager = manager
        self.commands = bot.get_command_manager()
