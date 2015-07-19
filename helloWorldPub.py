from testConfig import structureConfig
import pubSubDreamland as psdl
from multiprocessing import Process


structureName = structureConfig["structureName"]
serverIp = structureConfig["serverIp"]

structureNames = ['pi' + n for n in range(1, 7)]

send_port = '5560'
recv_port = '5559'

sub = psdl.Subscriber(serverIp, recv_port, structureName, isServer=True)
pub = psdl.Publisher(serverIp, send_port, structureName, isServer=True)


def sendMessageToClients():
    message = 'hello'
    while True:
        for structureName in structureNames:
            pub.sendMessage(structureName, message)


def receiveMessageFromClients():
    while True:
        publisherId, message = sub.recv_message()
        print('Received : ' + message + ' from ' + publisherId)

if __name__ == '__main__':
    Process(target=sendMessageToClients).start()
    Process(target=receiveMessageFromClients).start()
