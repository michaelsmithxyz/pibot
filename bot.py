#!/usr/bin/env python3

import socket
import sys

import events
import irc
import logging as l
import plugin
import poll

class Bot:
    def __init__(self, server, port, nick, args):
        self.server = server
        self.port = port
        self.nick = nick
        self.rbuffer = ""
        self.args = args
        self.mqueue = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bundle = (self, irc, l, events, args)
        self.poller = poll.Poller()
        self.plugin_manager = plugin.PluginManager(self.bundle)

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
        l.info("Sending initial info")
        self.send_message(irc.nick(self.nick))
        self.send_message(irc.user(self.nick, "Temporary Name"))
        self.poller.remove_write(self.sock)
        self.poller.add_write(self.sock, self.write_socket)

    def write_socket(self, poller, sock):
        if len(self.mqueue) > 0:
            msg = self.mqueue.pop(0)
            sock.send(bytes(msg, 'UTF-8'))
            self.plugin_manager.handle_event(events.WRITE_MESSAGE, [msg])

    def quit(self):
        self.sock.send(bytes(irc.quit(), 'UTF-8'))
        self.disconnect(self.poller, self.sock)

    def disconnect(self, poller, sock):
        l.info("Disconnecting")
        self.poller.remove_all(sock)
        sock.close()
        self.plugin_manager.handle_event(events.DISCONNECT, [])
        sys.exit(0)

    def send_message(self, message):
        self.mqueue.append(message)

    def main(self):
        self.plugin_manager.load("plugins/")
        self.sock.connect((self.server, self.port)) 
        self.poller.add_read(self.sock, self.read_socket)
        self.poller.add_write(self.sock, self.first_write)
        self.poller.add_except(self.sock, self.disconnect)
        try:
            self.poller.mainloop()
        except KeyboardInterrupt:
            self.quit()
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.disconnect(self.poller, self.sock)
