#!/usr/bin/env python

# Import basic packages
# import os
# import time
import sys
import zmq

# Take in IP from commandline, build string to connect to
ip = sys.argv[1]
port = 1111
string = "tcp://" + ip + ":" + str(port)

# Initialize the ZeroMQ Conext
context = zmq.Context()

# Configure ZeroMQ to recieve messages
zmq_recv = context.socket(zmq.SUB)


# Configure zmq connection
zmq_recv.connect(string)
zmq_recv.setsockopt_string(zmq.SUBSCRIBE, '')  # recieve string, subscribe to all

print("Connecting to Dreamland server at %s : %d" % (ip, port))

print("Pi Home Server ZeroMQ client running !")
