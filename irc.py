#!/usr/bin/env python3

def parse_message(message):
    prefix = ''
    split = message.split(' ')
    args = []
    if split[0][0] == ':':
        prefix = split[0]
        split = split[1:]
    command = split[0]
    split = split[1:]
    for x in split:
        if x[0] == ':':
            index = split.index(x)
            arg = ' '.join(split[index:])
            args.append(arg[1:])
            break
        args.append(x)
    return [prefix, command, args]

def parse_names(args):
    args = args[2]
    channel = args[2]
    return (channel, args[3].split(' '))

def parse_nick(name):
    parts = name.split('!')
    return (parts[0][1:], parts[1])

def raw_nick(name):
    if name[0] in ('@', '&', '~', '+', '%'):
        return name[1:]
    return name

def privmsg(rcpt, msg):
    return "PRIVMSG %s :%s\r\n" % (rcpt, msg)

def user(username, realname, mask=0):
    return "USER %s %d * :%s\r\n" % (username, mask, realname)

def nick(name):
    return "NICK %s\r\n" % (name)

def pong(msg):
    return "PONG :%s\r\n" % (msg)

def quit():
    return "QUIT\r\n"

def join(channel, key=None):
    if key is not None:
        return "JOIN %s %s\r\n" % (channel, key)
    return "JOIN %s\r\n" % (channel)

def part(channel, msg=None):
    if msg is not None:
        return "PART %s :%s\r\n" % (channel, msg)
    return "PART %s\r\n" % (channel)
