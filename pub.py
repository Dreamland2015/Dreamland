#!/usr/bin/env python3
from __future__ import print_function

import time
import random

import util

def doit():
    #pub = util.PubClient(master='localhost', topic=['carousel', 'thing'][random.randint(0,1)])
    l1 = util.PubClient(master='localhost', topic='lampPost1')
    l2 = util.PubClient(master='localhost', topic='lampPost2')
    l3 = util.PubClient(master='localhost', topic='lampPost2')
    #target = 'flame'
    target = 'button_light'
    l1.send(target, 1)
    l2.send(target, 1)
    l3.send(target, 1)
    time.sleep(.4)
    l1.send(target, 0)
    l2.send(target, 0)
    l3.send(target, 0)
    #pub.send('flame', random.randint(0,1))

if __name__ == '__main__':
    doit()

