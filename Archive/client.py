import zmq
import sys
import random
import time
from multiprocessing import Process

### User inputs 
####

# Configure ports
recv_port = "5560"
send_port = "5559"

# Configure server ip
ip_string = "tcp://" + sys.argv[1] + ":" + recv_port

# initialize ZMQ
context = zmq.Context()

# setup subscriber socket
zmq_recv = context.socket(zmq.SUB)
zmq_recv.connect(ip_string)

# setup publisher socket
zmq_send = context.socket(zmq.PUB)
zmq_send.bind("tcp://*:" + send_port)
publisher_id = random(0, 9999)


def Send_message(send_to):
	topic = random(1, 10)

	while True:
		message_send = "Server # " + publisher_id
		zmq_send.send_string(topic, message_send)
		time.sleep(1)


def Recv_message(sent_from, recv_message):
	zmq_recv.setsockopt_string(zmq.SUBSCRIBE, sent_from)

	while True:
		string = zmq_recv.recv_string()
		topic, message_recv = string.split()
		print(message_recv)

if __name__ == "__main__":
	Process(target=Send_message, )