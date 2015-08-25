import zmq
import time

import numpy as np

t = np.linspace(0, 2 * np.pi, 1000)
v = .1


port = "6000"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)
i = 0
while True:
    messagedata = str(t[i])
    i = i + 1
    topic = 'accel'
    sendString = "%s|%s,%i" % (topic, messagedata, v)
    print(sendString)
    socket.send_string(sendString)
    time.sleep(0.001)
    if i == len(t):
        i = 0
