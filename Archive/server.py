import zmq
import sys
import time

# Configure ports
send_port = "5560"
recv_port = "5559"

# Configure client ip
ip_string = "tcp://" + sys.argv[1] + ":" + recv_port

# Initialize ZMQ
context = zmq.Context()

# Configure publisher socket
zmq_send = context.socket(zmq.PUB)
zmq_send.bind("tcp://*:" + send_port)

# Configure subscriber socket
print("Connecting to : " + ip_string)
zmq_recv = context.socket(zmq.SUB)
zmq_recv.connect(ip_string)
zmq_recv.setsockopt_string(zmq.SUBSCRIBE, "")  # subscribe to all

while True:
	message_send = "Hello from server"
	zmq_send.send_string(message_send)
	time.sleep(1)
