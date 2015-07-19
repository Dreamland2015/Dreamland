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
    if message == '1':
        s.sendMessage('carousel', '0 high')
    elif message == '0':
        s.sendMessage('carousel', '0 low')
    else:
        print("WHAT YOU SAY?!")
    # structureName, message = message.split(',')
    # s.sendMessage(structureName, message)
