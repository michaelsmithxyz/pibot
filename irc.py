#!/usr/bin/env python3

def parse_message(message):
    parts = message.split(' ')
    final = None
    for i in range(1, len(parts)):
        if parts[i][0] == ':':
            final = i
            break
    if final is not None:
        parts[final] = parts[final][1:]
        return parts[:final] + [' '.join(parts[final:])]
    return parts

def privmsg(rcpt, msg):
    return "PRIVMSG %s :%s\r\n" %(rcpt, msg)

def user(username, realname, mask=0):
    return "USER %s %d * :%s\r\n" %(username, mask, realname)

def nick(name):
    return "NICK %s\r\n" %(name)

def pong(msg):
    return "PONG :%s\r\n" %(msg)

def quit():
    return "QUIT\r\n"
