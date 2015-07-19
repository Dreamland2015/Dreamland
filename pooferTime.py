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


def firePoofer(poofer, dwell, delay):
	pooferHigh(poofer)
	time.sleep(dwell)
	pooferLow(poofer)
	time.sleep(delay)


def pooferHigh(poofer):
	s.sendMessage(structureName, poofer + ' high')


def pooferLow(poofer):
	s.sendMessage(structureName, poofer + ' low')


def sequentialPoofer(poofers, onDelay, offDelay):
	for poofer in poofers:
		firePoofer(poofer, onDelay, offDelay)


def subOneToString(num):
	num = int(num) - 1
	return str(num)

def createRandomList():
	randomList
	for numPoofers in random.randint(0,3):
		randomList.append(random.random(0,3))

## sequential poofing
# for n in range(10):
# 	sequentialPoofer(['0', '1', '2', '3'], .1, .1)

# ## random number of poofers for 
# poofers = ['0', '1', '2', '3']
# startTime = time.time()
# while time.time()- startTime < 10:



while True:
	message = input('how long to fire?: ')
	poofer, loop, dwell, delay = message.split()
	poofer = subOneToString(poofer)
	for n in range(int(loop)):
		fireTime = float(dwell)
		firePoofer(poofer, fireTime, float(delay))
