#!/usr/bin/env python3

import imp
import inspect
import logging as l
import os

class PluginError(Exception):
    pass


class PluginManager(object):
    def __init__(self, bot):
        self.handlers = {}
        self.plugins = []
        self.bot = bot

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
                self._prepare_plugin(instance)
                l.info("Loaded plugin", instance.name)
        except Exception as e:
            l.err("Error loading module", name)
            l.err('\t', str(e))

    def _prepare_plugin(self, plugin):
        methods = [x[1] for x in inspect.getmembers(plugin, inspect.ismethod)]
        for method in methods:
            if hasattr(method, 'events'):
                for event in method.events:
                    l.info("Hooking event:", event, "in plugin", plugin.name)
                    self.add_handler(event, method)

    def _find_plugins(self, module, base):
        return [cls for name, cls in inspect.getmembers(module) if
            inspect.isclass(cls) and issubclass(cls, base)
            and cls is not base]

    def unload_all(self):
        for plug in self.plugins:
            self.unload_plugin(plug)

    def unload_plugin(self, plugin):
        plugin.unload()
        self.plugins.remove(plugin)

    def get_plugin(self, name):
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin
        return None

    def handle_event(self, event, args):
        if event in self.handlers:
            for handle in self.handlers[event]:
                handle(event, args)

    def add_handler(self, event, handler):
        if event in self.handlers:
            self.handlers[event].append(handler)
        else:
            self.handlers[event] = [handler]
    
    def remove_handler(self, event, handler):
        if handler in self.handlers:
            self.handlers[handler].remove(event)


class PiPlugin(object):
    def __init__(self, bot, manager):
        self.bot = bot
        self.manager = manager
        self.commands = bot.get_command_manager()
        
    def unload(self):
        pass

def hooks(events):
    if type(events) == str:
        events = [events]
    def _decor(function):
        function.events = events
        return function
    return _decor
