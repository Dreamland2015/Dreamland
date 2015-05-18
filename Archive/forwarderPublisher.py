import zmq
import random
import time

port = "2222"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:%s" % port)
publisher_id = random.randrange(0, 9999)
while True:
    topic = random.randrange(1, 10)
    messagedata = "server#" + publisher_id
    print "%s %s" % (topic, messagedata)
    socket.send_string("%d %s" % (topic, messagedata))
    time.sleep(1)
