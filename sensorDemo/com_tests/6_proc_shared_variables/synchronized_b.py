# -*- coding: utf-8 -*-
"""
Testing shared variables between processes.
Using demo from:
http://eli.thegreenplace.net/2012/01/04/shared-counter-with-pythons-multiprocessing
"""

import time
from multiprocessing import Process, Value, Array, Lock

class Gyrodata(object):
    def __init__(self, initdata=[1, 2, 33, 444, -5, -66, 70000]):
        self.rawdata = Array('i', initdata)
        # processed values: speed, angle
        self.data = Array('d', [123, 456])
        print("init: ", self.data[0])
        self.lock = Lock()

    def set_rawdata(self, rawdata):
        with self.lock:
            self.gyro_raw.value = rawdata

    def set_data(self, data):
        with self.lock:
            self.gyro.value = data

    def rawdata(self):
        with self.lock:
            return self.rawdata

    def data(self):
        with self.lock:
            return self.data


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
    gd = Gyrodata()
    procs = [Process(target=func, args=(counter,)) for i in range(2)]

    for p in procs: p.start()
    for p in procs: p.join()

    print("gd.data is: ", gd.rawdata[0])

    print(counter.value())
