from testConfig import structureConfig
import pubSubDreamland as psdl
from multiprocessing import Process
import time


name = structureConfig["structureName"]
serverIp = structureConfig["serverIp"]

structureNames = ['pi' + str(n) for n in range(1, 7)]

send_port = '5560'
recv_port = '5559'


def sendMessageToClients():
    pub = psdl.Publisher(serverIp, send_port, name, isServer=True)
    message = 'hello'
    while True:
        for structureName in structureNames:
            print(structureName)
            pub.sendMessage(structureName, message)
            time.sleep(1)


def receiveMessageFromClients():
    sub = psdl.Subscriber(serverIp, recv_port, name, isServer=True)
    while True:
        publisherId, message = sub.recvMessage()
        print('Received : ' + message + ' from ' + publisherId)

if __name__ == '__main__':
    Process(target=sendMessageToClients).start()
    Process(target=receiveMessageFromClients).start()
