#!/usr/bin/env python
import os
import sys
import time
import zmq

context = zmq.Context()

# Configure ZeroMQ to send messages
zmq_recv = context.socket(zmq.SUB)
# The communication is made on socket 1111
zmq_recv.connect("tcp://192.168.1.33:1111")

# Configure ZeroMQ to receive messages
zmq_send = context.socket(zmq.PUB)
# The communication is made on socket 1112
zmq_send.connect("tcp://192.168.1.33:1112")
zmq_recv.setsockopt(zmq.SUBSCRIBE, '')

print("Pi Home Server ZeroMQ client running !")

while True:
    print "Input value to send : "
    message = raw_input().strip()

    if message:
        try:
            print("Sending value : " + message zmq_send.send(message))
        except zmq.ZMQError as err:
            print("Error while trying to send the value " + message + " : " + str(err))

    try:
        incoming_message = zmq_recv.recv()
        print("Value received from the server : " + incoming_message)
    except zmq.Zmqerror as err:
        print(' Receive error: ' + str(err))
