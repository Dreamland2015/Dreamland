import paramiko
import sys
import time
from threading import Thread

serverIp = "10.0.1.165"

login = "pi"
password = "raspberry"

config = [
    {"hostname": "pi.local", "structureName": "carousel"},
    {"hostname": "pi1.local", "structureName": "bench1"},
    {"hostname": "pi2.local", "structureName": "bench2"}
]

config2 = {
    "Carousel": {"hostname": "pi.local",
                 "serverIp": serverIp},
    "Bench": {"hostname": "pi.local",
              "serverIp": serverIp}
}


def doSomethingHere():
    pass


def writeConfigFile():
    f = open("config.py", "w")

    var = {"structureName": "yourMom",
           "hotname": "pi@pi.local",
           "serverIP": "8.8.8.8"}

    for k, v in var.items():
        f.write('{} = "{}"\n'.format(k, v))


class SSHConnection():
    def __init__(self, hostname, structureName):
        self.hostname = hostname
        self.structureName = structureName
        self.connectToSSH()

    def connectToSSH(self):
        for x in range(10):
            try:
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(self.hostname, username=login, password=password)
                print ("Connected to " + self.structureName)
                break
            except paramiko.AuthenticationException:
                print ("Authentication failed when connecting to " + self.structureName)
                sys.exit(1)
            except:
                print ("Could not SSH to " + self.structureName + ", waiting for it to start")
                time.sleep(1)
        return

        # If no connection in the allowed time.
        raise RuntimeError("Could not connect to " + self.structureName + ". Giving up")

    def runCommand(self, commandToRun):
        stdin, stdout, stderr = self.ssh.exec_command(commandToRun)


class MultiSSH:
    def __init__(self, listOfStructures):
        self.listOfStructures = listOfStructures
        self.sshConnections = []
        for structure in listOfStructures:
            self.sshConnections.append(SSHConnection(structure["hostname"], structure["structureName"]))
        # self.runOnAll()

    def runOnAll(self, commandToRun):
        running = []
        for connection in self.sshConnections:
            # Arbitraily complicated stuff
            th = Thread(target=connection.connectToSSH.runCommand(commandToRun))
            running.append(th)

        for r in running:
            r.join()

    def runOnGroup(self, groupDescriptor, commandToRun):
        pass

    def runMultipleCommandsOnAll(self, commandList):
        pass

    def setupConfigFile(self, stuffIWantInThere):
        self.runOnAll("echo SOME TERRIBLE STRING I MAKE IN CODE > config.py")
