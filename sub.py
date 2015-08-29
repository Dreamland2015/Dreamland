#!/usr/bin/env python
from __future__ import print_function

import util

def doit():
    sub = util.SubClient('localhost')
    while True:
        print('recv', sub.recv(raw=True))

if __name__ == '__main__':
    doit()
