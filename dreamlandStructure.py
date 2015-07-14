from testConfig import structureConfig
import pubSubDreamland as psdl
# import gpioDreamland as ioDL
import gpioDreamland as ioDL

structureName = structureConfig["structureName"]
serverIp = structureConfig["serverIp"]

recv_port = '5560'
send_port = '5559'

sub = psdl.Subscriber(serverIp, recv_port, structureName, isServer=False)
pub = psdl.Publisher(serverIp, send_port, structureName, isServer=False)

outputPins = ioDL.stringToList(structureConfig['outputPins'])

ioDL.setMode()
outputPins = [ioDL.Poofer(pin) for pin in outputPins]

while True:
		poofer, command = sub.recvMessage().split()
		if command == 'high':
			print('using pin ' + poofer + ' high')
			outputPins[int(poofer)].high()
		elif command == 'low':
			print('using pin ' + poofer + ' low')
			outputPins[int(poofer)].low()
		else:
			print('WHAT YOU SAY?!')
			pass
