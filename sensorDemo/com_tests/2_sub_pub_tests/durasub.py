# -*- coding: utf-8 -*-
"""
Modified from
http://stackoverflow.com/questions/8092473/zeromq-high-water-mark-doesnt-work
"""

import zmq
import time

context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.setsockopt(zmq.IDENTITY, b"Hello")
subscriber.setsockopt(zmq.SUBSCRIBE, b"")
subscriber.connect("tcp://localhost:5565")

print("started subscriber", flush=True)

#sync = context.socket(zmq.PUSH)
#sync.connect("tcp://localhost:5564")
#print("started sync socket, waiting on sync", flush=True)
#sync.send(b"")
#print("sent sync", flush=True)

start = time.time()
while True:
    data = subscriber.recv()
    print("Received data is: ", data, flush=True)
    now = time.time()
#    print("time is:", now, flush=True)
    time.sleep(1)
    if data == b"END" or (now-start)>60:
        break
