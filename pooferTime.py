from testConfig import structureConfig
import pubSubDreamland as psdl
import random
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


def multiPooferHigh(poofers):
    for poofer in poofers:
        pooferHigh(poofer)


def pooferLow(poofer):
    s.sendMessage(structureName, poofer + ' low')


def multiPooferLow(poofers):
    for poofer in poofers:
        pooferLow(poofer)


def sequentialPoofer(poofers, onDelay, offDelay):
    for poofer in poofers:
        firePoofer(poofer, onDelay, offDelay)


def subOneToString(num):
    num = int(num) - 1
    return str(num)


def createRandomList():
    randomList = random.sample(range(4), random.randint(0, 4))
    randomList = [str(i) for i in randomList]
    return randomList

# sequential poofing
# for n in range(10):
#       sequentialPoofer(['0', '1', '2', '3'], .1, .1)

# random number of poofers for
poofers = ['0', '1', '2', '3']
startTime = time.time()
for n in range(5):
    poofers = createRandomList()
    multiPooferHigh(poofers)
    time.sleep(0.02)
    multiPooferLow(poofers)
    time.sleep(0.06)

# while True:
#       message = input('how long to fire?: ')
#       poofer, loop, dwell, delay = message.split()
#       poofer = subOneToString(poofer)
#       for n in range(int(loop)):
#               fireTime = float(dwell)
#               firePoofer(poofer, fireTime, float(delay))
