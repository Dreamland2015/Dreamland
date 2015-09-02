import util
import time

serverIp = util.get_default_ip()

# output = util.output

pub = util.PubClient(serverIp, 'carousel-top')

poofList = ['flame1', 'flame2', 'flame3', 'center']

def sendPoofCenter(poofer, delay):
	print("poof")
	pub.send(poofer,0)
	time.sleep(delay)
	pub.send(poofer,1)
	time.sleep(delay)

while True:
	for poofer in poofList:
		sendPoof(poofer, 0.05)
	