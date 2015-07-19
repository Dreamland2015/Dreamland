# -*- coding: utf-8 -*-
"""
Modified from
http://stackoverflow.com/questions/8092473/zeromq-high-water-mark-doesnt-work

Run this, and run durasub.py in another shell.

"""

import zmq
import time

context = zmq.Context()

# create publisher socket,
publisher = context.socket(zmq.PUB)
# set high water mark = max # of msg to buffer
# needs to be zmq.SNDHWM or zmq.RCVHWM in zmq 3, not zmq.HWM
publisher.setsockopt(zmq.SNDHWM, 2)
publisher.setsockopt(zmq.RCVHWM, 2)
sock.setsockopt(zmq.LINGER, 1000)
publisher.bind("tcp://*:5565")
print("started publisher", flush=True)

# Wait till subscriber program has started and sent a ready message:
# to the socket "sync". After that the program continues, and are
# synchronized.
#sync = context.socket(zmq.PULL)
#sync.bind("tcp://*:5564")
#print("Waiting for ready signal from subscriber thread", flush=True)
#sync_request = sync.recv()
#print("Got sync", flush=True)

for n in range(100):
    msg = ("Update %d" % n).encode('ascii')
    publisher.send(msg)
    print("n is ", n, flush=True)
    time.sleep(0.1)

publisher.send(b"END")
