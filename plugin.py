#!/usr/bin/env python3

import abc
import imp
import inspect
import logging as l
import os
import os.path

class PluginError(Exception):
    pass

class PluginManager:
    PLUGINS = []
    HOOKS = {}
    def __init__(self, bot):
        self.bot = bot

    @classmethod
    def hook_event(cls, event):
        def _decor(function):
            cls.add_handler(cls, event, function)
            def wrapper(*args, **kwargs):
                function(*args, **kwargs)
            return wrapper
        return _decor

    def add_handler(self, event, handler):
        if handler in self.HOOKS:
            self.HOOKS[event].append(handler)
        else:
            self.HOOKS[event] = [handler]
    
    def remove_handler(self, event, handler):
        if event in self.HOOKS:
            if handler in self.HOOKS[event]:
                self.hooks[event].remove(handler)

    def handle_event(self, event, args):
        if event in self.HOOKS:
            for handler in self.HOOKS[event]:
                handler(event, args)

    def enable_all(self):
        for plugin in self.PLUGINS:
            self.enable(plugin)

    def disable_all(self):
        for plugin in self.PLUGINS:
            self.disable(plugin)

    def enable(self, plugin):
        plugin.enable()

    def disable(self, plugin):
        plugin.disable()

    def reload(self, plugin):
        if plugin in self.PLUGINS:
            plugin.disable()
            plugin.enable()

    def get_plugin(self, name):
        for plugin in self.PLUGINS:
            if plugin.name.lower() == name.lower():
                return plugin
        return None
    
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
            self._load_module(full_name, mod_info)

    def _load_module(self, name, info):
        try:
            mod = imp.load_module(name, *info)
            plugins = self._find_plugins(mod, PiPlugin)
            for plugin in plugins:
                instance = plugin(self.bot, self)
                if not hasattr(instance, "name"):
                    raise PluginError("Plugin %s does not have a defined name" % instance)
                self.PLUGINS.append(instance)
                l.info("Loaded module", instance.name)
        except Exception as e:
            l.warn("Error loading module", name)
            l.warn("\t", str(e))

    def _find_plugins(self, module, base):
        return [cls for name, cls in inspect.getmembers(module) if 
                inspect.isclass(cls) and issubclass(cls, base) 
                and cls is not base]

class PiPlugin:
    def __init__(self, bot, manager):
        self.manager = manager
        self.commands = bot.get_command_manager()
        self.bot = bot

    def enable(self):
        pass

    def disable(self):
        pass
