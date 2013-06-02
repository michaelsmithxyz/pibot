#!/usr/bin/python3

import select
import time

class Poller(object):
    def __init__(self):
        self.write_mapping = {}
        self.read_mapping = {}
        self.except_mapping = {}

    def add_read(self, fhandle, callback):
        self.read_mapping[fhandle] = callback

    def add_write(self, fhandle, callback):
        self.write_mapping[fhandle] = callback

    def add_except(self, fhandle, callback):
        self.except_mapping[fhandle] = callback

    def add_all(self, fhandle, callback):
        self.add_read(fhandle, callback)
        self.add_write(fhandle, callback)
        self.add_except(fhandle, callback)

    def remove_read(self, fhandle):
        if fhandle in self.read_mapping:
            del self.read_mapping[fhandle]

    def remove_write(self, fhandle):
        if fhandle in self.write_mapping:
            del self.write_mapping[fhandle]

    def remove_except(self, fhandle):
        if fhandle in self.except_mapping:
            del self.except_mapping[fhandle]

    def remove_all(self, fhandle):
        self.remove_read(fhandle)
        self.remove_write(fhandle)
        self.remove_except(fhandle)

    def total_fhandles(self):
        w = len(self.write_mapping)
        r = len(self.read_mapping)
        e = len(self.except_mapping)
        return w + r + e

    def mainloop(self, wait=0):
        while self.total_fhandles() > 0:
            rds, wrts, xcpts = select.select(
                list(self.read_mapping.keys()),
                list(self.write_mapping.keys()),
                list(self.except_mapping.keys())
                )
            for r in rds:
                self.read_mapping[r](self, r)
                for w in wrts:
                    self.write_mapping[w](self, w)
                for e in xcpts:
                    self.except_mapping[e](self, e)
            time.sleep(wait)
