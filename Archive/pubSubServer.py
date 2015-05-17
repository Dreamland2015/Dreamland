#!/usr/bin/env python

#   Dreamland output server
#   Binds PUB socket to tcp://*:5556
#   Publishes effect outputs to network
#

import zmq
import time


context = zmq.Context()

zmq_send = context.socket(zmq.PUB)
zmq_send.bind("tcp://*:1111")

while True:
    dreamLandObject = "bench1"

    for number in range(10):
        zmq_send.send_string("%s %i " % (dreamLandObject, number))
        print(str(number))
        time.sleep(1)
