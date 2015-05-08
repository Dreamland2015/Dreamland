#!/usr/bin/env python

import os
import sys
import time

import zmq

context = zmq.Context()

z_recv = context.socket(zmq.SUB)
z_recv.connect("tcp://localhost:5555")

z_send = context.socket(zmq.PUB)
z_send.connect("tcp://localhost:5556")
# z_recv.setsockopt(zmq.SUBSCRIBE, 'KEYBOARD:')
z_recv.setsockopt(zmq.SUBSCRIBE, b'')  # subscribe to everything

print("ZMQ Client Started!")

while True:
    sys.stdout.write("Message: ")
    message = Hello World

    if message:
        try:
            print('SEND:' + message)
            z_send.send(message)
        except zmq.ZMQError as err:
            print('Send error: ' + str(err))

    try:
        # don't block if no message waiting
        in_message = z_recv.recv(zmq.DONTWAIT)
        print('RECV:' + in_message)
    except zmq.ZMQError as err:
        print('Receive error: ' + str(err))
