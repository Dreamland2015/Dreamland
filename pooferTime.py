from testConfig import structureConfig
import pubSubDreamland as psdl
import random
import time

pooferList = ['0', '1', '2', '3']

structureName = structureConfig["structureName"]
structureName = 'poofTest'
serverIp = structureConfig["serverIp"]

send_port = '5560'
recv_port = '5559'

r = psdl.Subscriber(serverIp, recv_port, 'server', isServer=True)
s = psdl.Publisher(serverIp, send_port, 'server', isServer=True)

print('sleep to make sure sockets are up')
time.sleep(1)

messageDelay = 0.001


def firePoofer(poofer, dwell, delay):
    pooferHigh(poofer)
    time.sleep(dwell)
    pooferLow(poofer)
    time.sleep(delay)


def multiFirePoofer(poofers, onDelay, offDelay):
    multiPooferHigh(poofers)
    time.sleep(onDelay)
    multiPooferLow(poofers)
    time.sleep(offDelay)


def pooferHigh(poofer):
    s.sendMessage(structureName, poofer + ' high')
    time.sleep(messageDelay)


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


def multiSequentialPoofing(listOfPoofers, onDelay, offDelay):
    for poofers in listOfPoofers:
        for poofer in poofers:
            print(poofer)
        multiPooferHigh(poofers)
        time.sleep(onDelay)
        multiPooferLow(poofers)
        time.sleep(offDelay)


def subOneToString(num):
    num = int(num) - 1
    return str(num)


def createRandomList():
    randomList = random.sample(range(4), random.randint(0, 4))
    randomList = [str(i) for i in randomList]
    return randomList

# # sequential poofing
# for n in range(10):
#     sequentialPoofer(pooferList, .05, .5)

# sequtional multipoofers
# listOfListOfPoofers = [['0', '2'], ['1', '3']]
# for n in range(4):
#     for listOfPoofers in listOfListOfPoofers:
#         multiSequentialPoofing(listOfPoofers, 0.02, 0.1)

# for n in range(2):
#     multiPooferHigh(pooferList)
#     time.sleep(0.02)
#     multiPooferLow(pooferList)
#     time.sleep(0.5)

# # random number of poofers for
# poofers = ['0', '1', '2', '3']
# startTime = time.time()
# for n in range(50):
#     poofers = createRandomList()
#     multiPooferHigh(poofers)
#     time.sleep(0.02)
#     multiPooferLow(poofers)
#     time.sleep(0.06)

while True:
    message = input('how long to fire?: ')
    poofer, loop, dwell, delay = message.split()
    poofer = subOneToString(poofer)
    for n in range(int(loop)):
        fireTime = float(dwell)
        firePoofer(poofer, fireTime, float(delay))
