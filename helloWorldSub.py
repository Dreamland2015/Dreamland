from structureConfig import structureConfig
import pubSubDreamland as psdl
# import gpioDreamland as ioDL
import fakeGPIO as ioDL

structureName = structureConfig["structureName"]
serverIp = structureConfig["serverIp"]

recv_port = '5560'
send_port = '5559'

sub = psdl.Subscriber(serverIp, recv_port, structureName, isServer=False)
pub = psdl.Publisher(serverIp, send_port, structureName, isServer=False)

outputPins = ioDL.stringToList(structureConfig['outputPins'])
print(outputPins)

ioDL.setMode()
outputPins = [ioDL.Poofer(pin) for pin in outputPins]

while True:
    command = sub.recvMessage().split()
    print(command)
