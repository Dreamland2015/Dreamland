# -*- coding: utf-8 -*-
"""
Testing shared variables between processes.

Using demo from:
http://eli.thegreenplace.net/2012/01/04/shared-counter-with-pythons-multiprocessing
"""

import time
from multiprocessing import Process, Value

def func(val):
    for i in range(50):
        time.sleep(0.01)
        val.value += 1

if __name__ == '__main__':
    v = Value('i', 0)
    procs = [Process(target=func, args=(v,)) for i in range(10)]

    for p in procs: p.start()
    for p in procs: p.join()

    print(v.value)
