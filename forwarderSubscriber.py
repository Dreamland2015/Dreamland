import sys
import zmq

port = "5560"
dreamlandObject = "9"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
print("Collecting updates from Dreamland servers...")

socket.connect("tcp://localhost:%s" % port)

socket.setsockopt(zmq.SUBSCRIBE, dreamlandObject)

while True:
	recievedString = socket.recv_string()
	subscribed, command = recievedString.split()
	print(command)
