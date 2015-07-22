#!/usr/bin/env python
from __future__ import print_function

import util

def doit():
    sub = util.SubClient('localhost', 'thing')
    while True:
        print('recv', sub.recv())

if __name__ == '__main__':
    doit()
