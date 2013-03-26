#!/usr/bin/env python3

def parse_message(message):
    prefix = ''
    split = message.split(' ')
    args = []
    if split[0][0] == ':':
        prefix = split[0]
    command = split[1]
    for x in split[2:]:
        if x[0] == ':':
            args.append(x[1:])
            break
        args.append(x)
    return [prefix, command, args]

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

def join(channel, key=None):
    if key is not None:
        return "JOIN %s %s\r\n" %(channel, key)
    return "JOIN %s\r\n" %(channel)

def part(channel, msg=None):
    if msg is not None:
        return "PART %s :%s\r\n" %(channel, msg)
    return "PART %s\r\n" %(channel)
