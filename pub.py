from __future__ import print_function

import time
import random

import util

def doit():
    pub = util.PubClient('localhost', ['one', 'thing'][random.randint(0,1)])
    msg = '%d-%d'%(random.randint(1,100), random.randint(1000,2000))
    pub.send(msg)

if __name__ == '__main__':
    doit()

