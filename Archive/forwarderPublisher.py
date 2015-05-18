import zmq
import random
import time

port = "5559"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:" + port)
publisher_id = random.randrange(0, 9999)
while True:
    topic = random.randrange(1, 10)
    messagedata = "server#" + str(publisher_id)
    print("%s %s" % (topic, messagedata))
    socket.send_string("%d %s" % (topic, messagedata))
    time.sleep(1)
