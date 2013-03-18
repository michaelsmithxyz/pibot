#!/usr/bin/env python3

import getopt
import sys

import bot

def usage():
    print("main.py -s [server] -p [port] -n [nick]")

def main(argv):
    server = 'irc.freenode.net'
    port = 6667
    nick = 's0lderbot'
    try:
        opts, args = getopt.getopt(argv, 's:n:p:')
    except:
        usage()
        return 1
    for o, a in opts:
        if o == '-s':
            server = a
        elif o == '-p':
            port = int(a)
        elif o == '-n':
            nick = a
    ircbot = bot.Bot(server, port, nick, opts)
    ircbot.main()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
