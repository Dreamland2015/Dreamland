import time
import zmq

ctx = zmq.Context()
pub = ctx.socket(zmq.PUB)
sub = ctx.socket(zmq.SUB)

url = "tcp://127.0.0.1:5555"
pub.bind(url)
sub.connect(url)

# subscribe to 'a' and 'b'
sub.setsockopt_string(zmq.SUBSCRIBE, 'a')
sub.setsockopt_string(zmq.SUBSCRIBE, 'b')

time.sleep(1)


while True:
	pub.send_string('a')
	time.sleep(1)
	print('receiving')
	print(sub.recv(zmq.NOBLOCK))
