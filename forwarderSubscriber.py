import sys
import zmq

port = "5560"
# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
print("Collecting updates from Dreamland servers...")
socket.connect("tcp://localhost:%s" % port)
topicfilter = b"9"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
for update_nbr in range(2):
    string = socket.recv()
    topic, messagedata = string.split()
    print(topic, messagedata)
