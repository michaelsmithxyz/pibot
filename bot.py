#!/usr/bin/env python3

import socket
import sys

import commands
import config
import events
import irc
import logging
import plugin
import poll

class Bot(object):
    def __init__(self, conf, args):
        self.rbuffer = ""
        self.args = args
        self.mqueue = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conffile = conf
        self.logger = logging.getLogger()
        self.conf = config.Config(self)
        self.conf.read(self.conffile)
        self.poller = poll.Poller()
        self.plugin_manager = plugin.PluginManager(self)
        self.command_manager = commands.CommandManager(self)

    def get_nick(self):
        return self.nick

    def get_connection(self):
        return self.connection

    def get_plugin_manager(self):
        return self.plugin_manager

    def get_command_manager(self):
        return self.command_manager

    def get_config(self):
        return self.conf

    def get_args(self):
        return self.args

    def get_poller(self):
        return self.poller

    def read_socket(self, poller, sock):
        r = sock.recv(1024)
        r = r.decode('UTF-8')
        self.rbuffer += r
        self.parts = self.rbuffer.split('\r\n')
        if len(self.parts) < 1:
            pass
        else:
            self.rbuffer = self.parts[-1]
            for msg in self.parts[:-1]:
                self.plugin_manager.handle_event(events.READ_MESSAGE, [msg])

    def first_write(self, poller, sock):
        self.logger.info("Sending initial info")
        self.send_message(irc.nick(self.conf.get_value("bot.nick")))
        self.send_message(irc.user(self.conf.get_value("bot.nick"),
                self.conf.get_value("bot.realname")))
        self.poller.remove_write(self.sock)
        self.poller.add_write(self.sock, self.write_socket)
        self.plugin_manager.handle_event(events.POST_CONNECT, [])

    def write_socket(self, poller, sock):
        if len(self.mqueue) > 0:
            msg = self.mqueue.pop(0)
            sock.send(bytes(msg, 'UTF-8'))
            self.plugin_manager.handle_event(events.WRITE_MESSAGE, [msg])

    def disconnect(self, poller, sock):
        self.terminate()
    
    def dump_queue(self):
        self.logger.info("Dumping message queue")
        while len(self.mqueue) > 0:
            msg = self.mqueue.pop(0)
            self.sock.send(bytes(msg, 'UTF-8'))

    def quit(self):
        self.plugin_manager.handle_event(events.EXIT, [])
        self.send_message(irc.quit())
    
    def _quit(self):
        try:
            self.sock.send(bytes(irc.quit(), 'UTF-8'))
        except:
            pass
        self.terminate()

    def terminate(self):
        self.logger.info("Terminating bot")
        self.plugin_manager.unload_all()
        self.poller.remove_all(self.sock)
        self.sock.close()
        sys.exit(0)

    def send_message(self, message):
        self.mqueue.append(message)

    def main(self):
        logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)
        req = self.conf.check([
            "bot.nick",
            "bot.realname",
            "bot.server",
            "bot.port"
            ])
        if len(req) > 1:
            self.logger.error("Cannot start bot. Missing required options:")
            for r in req:
                l.err("\t", r)
            sys.exit(1)
        self.plugin_manager.load("modules/")
        pldir = self.conf.get_value("bot.plugindir")
        if pldir is not None:
            self.plugin_manager.load(pldir)
        self.nick = self.conf.get_value("bot.nick")
        self.connection = (self.conf.get_value("bot.server"),
                int(self.conf.get_value("bot.port")))
        self.logger.info("Connecting...")
        self.sock.connect(self.connection)
        self.poller.add_read(self.sock, self.read_socket)
        self.poller.add_write(self.sock, self.first_write)
        self.poller.add_except(self.sock, self.disconnect)
        try:
            self.poller.mainloop()
        except KeyboardInterrupt:
            self.quit()
            self.dump_queue()
            self.terminate()
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.terminate()
