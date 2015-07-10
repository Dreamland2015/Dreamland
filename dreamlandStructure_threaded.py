from testConfig import structureConfig
import pubSubDreamland as psdl

structureName = structureConfig["structureName"]
serverIp = structureConfig["serverIp"]

recv_port = '5560'
send_port = '5559'

r = psdl.Subscriber(serverIp, recv_port, structureName, isServer=False)
s = psdl.Publisher(serverIp, send_port, structureName, isServer=False)

while True:
	message = input('Send structures name, command: ')
	structureName, message = message.split(',')
	s.sendMessage(structureName, message)
