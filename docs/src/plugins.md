Plugin Development
==================

piBot is fully extensible with an event based plugin system. In fact, many
core piBot functionality is implemented using the same priciples (internal
plugins are called modules).

piBot plugins are written in Python, and access to the bot is provided with
a simple API. Most of the work involved in writing a plugin will be in dealing
with the event system.

Getting Started
---------------

The most basic piBot plugin looks like this:

    NAME = "testplugin"

    class Plugin:
        def __init__(self, bot):
            self.bot = bot

        def init(self):
            pass

    def init(bot):
        pl = Plugin(bot)
        return pl

The plugin system loads your module, and calls the `init` function, which it
expects to return the plugin (in this case an instance of `Plugin`). All
plugin files must have the extension `.mod.py`. They will not be loaded
otherwise. Likewise, the `NAME` attribute is required in all plugin modules.

After all other plugins are loaded, the `init` function of the plugin will be
called. This is where events would be registered, among other things.

Saving this plugin and starting piBot should result in a message being logged
indicating that the plugin `testplugin` has been loaded.
