#!/usr/bin/env python3
from __future__ import print_function

import time
import random

import util

def doit():
    pub = util.PubClient(master='localhost', topic=['carousel', 'thing'][random.randint(0,1)])
    pub.send(['center', 'side'][random.randint(0,1)], random.randint(0,1))

if __name__ == '__main__':
    doit()

