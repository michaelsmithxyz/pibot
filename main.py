#!/usr/bin/env python3

import getopt
import sys

import bot

def usage():
    print("main.py -c [config file]")

def main(argv):
    conf = 'bot.conf'
    try:
        opts, args = getopt.getopt(argv, 'c:')
    except:
        usage()
        return 1
    for o, a in opts:
        if o == '-c':
            conf = a
    ircbot = bot.Bot(conf, opts)
    ircbot.main()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
