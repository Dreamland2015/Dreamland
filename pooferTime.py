from testConfig import structureConfig
import pubSubDreamland as psdl
import time


structureName = structureConfig["structureName"]
serverIp = structureConfig["serverIp"]

send_port = '5560'
recv_port = '5559'

r = psdl.Subscriber(serverIp, recv_port, 'server', isServer=True)
s = psdl.Publisher(serverIp, send_port, 'server', isServer=True)

print('sleep to make sure sockets are up')
time.sleep(1)


def firePoofer(dwell, delay):
	s.sendMessage('carousel', '0 high')
	time.sleep(dwell)
	s.sendMessage('carousel', '0 low')
	time.sleep(delay)

while True:
	message = input('how long to fire?: ')
	loop, dwell, delay = message.split()

	for n in range(int(loop)):
		fireTime = float(dwell)
		firePoofer(fireTime, float(delay))
