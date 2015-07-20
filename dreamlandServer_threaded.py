from testConfig import structureConfig
import pubSubDreamland as psdl


structureName = structureConfig["structureName"]
serverIp = structureConfig["serverIp"]

send_port = '5560'
recv_port = '5559'

r = psdl.Subscriber(serverIp, recv_port, 'server', isServer=True)
s = psdl.Publisher(serverIp, send_port, 'server', isServer=True)

while True:
    message = input('Send structures name, command: ')
    # s.sendMessage(message)
    structureName, message = message.split(',')
    s.sendMessage(structureName, message)
    rMessage = r.recvMessage()
    print(rMessage)
