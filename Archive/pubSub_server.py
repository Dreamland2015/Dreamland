#!/usr/bin/env python

# Import basic packages
# import os
# import sys
import time
import zmq

# Initialize the ZeroMQ context
context = zmq.Context()

# Configure ZeroMQ to send messages
zmq_send = context.socket(zmq.PUB)

# The communication is made on socket 1111
zmq_send.bind("tcp://*:1111")
print ("Sending messages on tcp://*:1111")

print ("Pi Home Server ZeroMQ server running !")

while True:
    stringToSend = "Hellow World"
    zmq_send.send_string(stringToSend)
    print(stringToSend)
    time.sleep(1)
