#!/usr/bin/env python3

import sys

OUTPUT = sys.stdout

def err(*args):
    msg = ' '.join(map(str, args))
    print("[Error] %s" %(msg), file=OUTPUT)

def warn(*args):
    msg = ' '.join(map(str, args))
    print("[Warning] %s" %(msg), file=OUTPUT)

def info(*args):
    msg = ' '.join(map(str, args))
    print("[Info] %s" %(msg), file=OUTPUT)
