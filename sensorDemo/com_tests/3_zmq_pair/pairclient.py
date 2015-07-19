import zmq
import random
import sys
import time

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)    # so we can interrupt w ctrl-C

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:%s" % port)

while True:
    msg = socket.recv()
    print(msg)
    socket.send_string("client message to server1")
    socket.send_string("client message to server2")
    time.sleep(1)
