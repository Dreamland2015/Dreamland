#!/usr/bin/env python
import os
import sys
import time
import zmq

context = zmq.Context()

# Configure ZeroMQ to send messages
zmq_recv = context.socket(zmq.SUB)
# The communication is made on socket 1111
zmq_recv.connect("tcp://127.0.0.1:1111")

# Configure ZeroMQ to receive messages
zmq_send = context.socket(zmq.PUB)
# The communication is made on socket 1112
zmq_send.connect("tcp://127.0.0.1:1112")
zmq_recv.setsockopt_string(zmq.SUBSCRIBE, '')

print("Pi Home Server ZeroMQ client running !")

while True:
    message = input("Input value to send : ")

    if message:
        try:
            print("Sending value : " + message)
            zmq_send.send_string(message)
        except zmq.ZMQError as err:
            print("Error while trying to send the value " + message + " : " + str(err))

        try:
            incoming_message = zmq_recv.recv_string()
            print("Value received from the server : " + incoming_message)
        except zmq.ZMQError as err:
            print(' Receive error: ' + str(err))


# if message:
#  try:
#      print("Sending value : " + message zmq_send.send(message))
#  except zmq.ZMQError as err:
#      print("Error while trying to send the value " + message + " : " + str(err))

#  try:
#      incoming_message = zmq_recv.recv()
#      print("Value received from the server : " + incoming_message)
#  except zmq.Zmqerror as err:
#      print(' Receive error: ' + str(err))
