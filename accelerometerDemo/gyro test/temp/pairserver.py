import zmq
import random
import sys
import time

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)	# so we can interrupt w ctrl-C

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:%s" % port)

i=0
while True:
    i=i+1
    sendstr = "Server message %d to client3" % i
    socket.send_string(sendstr)
    msg = socket.recv()
    print(msg)
    time.sleep(0.1)