# -*- coding: utf-8 -*-
"""
Testing shared variables between processes.
Using demo from:
http://eli.thegreenplace.net/2012/01/04/shared-counter-with-pythons-multiprocessing
"""

import time
from multiprocessing import Process, Value, Lock

class Counter(object):
    def __init__(self, initval=0):
        self.val = Value('i', initval)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def value(self):
        with self.lock:
            return self.val.value

def func(counter):
    for i in range(50):
        time.sleep(0.01)
        counter.increment()

if __name__ == '__main__':
    counter = Counter(0)
    procs = [Process(target=func, args=(counter,)) for i in range(10)]

    for p in procs: p.start()
    for p in procs: p.join()

    print(counter.value())