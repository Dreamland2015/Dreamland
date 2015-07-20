from structureConfig import structureConfig
import pubSubDreamland as psdl

structureName = structureConfig["structureName"]
serverIp = structureConfig["serverIp"]

recv_port = '5560'
send_port = '5559'

sub = psdl.Subscriber(serverIp, recv_port, structureName, isServer=False)
pub = psdl.Publisher(serverIp, send_port, structureName, isServer=False)

while True:
    command = sub.recvMessage()
    print(command)
    pub.sendMessage('server', 'world')
