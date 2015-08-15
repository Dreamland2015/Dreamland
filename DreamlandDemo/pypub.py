import zmq
import time

import numpy as np

t = np.linspace(0, 2 * np.pi, 1000)
v = 30


port = "6000"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)
i = 0
while True:
    messagedata = str(t[i])
    i = i + 1
    topic = 'testing'
    print("%s, %i" % (messagedata, v))
    socket.send_string("%s, %s, %i" % (topic, messagedata, v))
    time.sleep(0.001)
    if i == len(t):
        i = 0
