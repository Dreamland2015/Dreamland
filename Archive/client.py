import zmq
import random
import time

port = "5556"


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:" + port)

while True:
    topic = "10001"
    messagedata = random.randrange(1, 215) - 80
    print("%s %d" % (topic, messagedata))
    socket.send_string("%s %d" % (topic, messagedata))
    time.sleep(1)
