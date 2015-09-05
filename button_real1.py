#!/usr/bin/env python
from __future__ import print_function

import time
import util

def doit():
    l1 = util.PubClient(master='localhost', topic='lampPost1')
    target = 'button_real'

    sub = util.SubClient('localhost', '')
    lp1_flame = False
    lp1_flame_time = time.time()
    while True:
        raw_recv = sub.recv(raw=True)
        topic, data = raw_recv.split('|')
        if topic == 'lampPost1':
            which, raw_value = data.split('#')
            value = int(raw_value)
            if which == 'flame':
                if value == '1':
                    lp1_flame = True
                else:
                    lp1_flame = False
                    lp1_flame_time = time.time()
            if which == 'button':
                #print('w', which, 'v', value)
                if lp1_flame is True:
                    continue
                if (time.time() - lp1_flame_time) < .1:
                    print("skipping press")
                    continue
                l1.send(target, value)
                print('sending l1', target, value)

if __name__ == '__main__':
    doit()
