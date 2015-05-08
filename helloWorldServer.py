#!/usr/bin/env python

import os
import sys
import time

import zmq

# ZMQ context, only need one per application
context = zmq.Context()

# for sending messages
z_send = context.socket(zmq.PUB)
z_send.bind("tcp://*:5555")

# for receiving messages
z_recv = context.socket(zmq.SUB)
z_recv.bind("tcp://*:5556")
z_recv.setsockopt(zmq.SUBSCRIBE, '')  # subscribe to everything

print "ZMQ server started."
while True:
    message = None

    # wait for incoming message
    try:
        message = z_recv.recv()
    except zmq.ZMQError as err:
        print("Receive error: " + str(err))

    # replay message to all subscribers
    if message:
        try:
            z_send.send(message)
        except zmq.ZMQError as err:
            print("Send error: " + str(err))
