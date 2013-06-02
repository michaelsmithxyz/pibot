#!/usr/bin/env python3

import getopt
import sys

import bot

def usage():
    print("main.py -c [config file]")

def main(argv):
    conf = 'bot.conf'
    try:
        opts = getopt.getopt(argv, 'c:')[0]
    except Exception:
        usage()
        return 1
    for opt, arg in opts:
        if opt == '-c':
            conf = arg
    ircbot = bot.Bot(conf, opts)
    ircbot.main()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
