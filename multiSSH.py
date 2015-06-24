import paramiko
import sys
import time
from threading import Thread

serverIp = "10.0.1.165"

login = "pi"
password = "raspberry"

config = [
    {"hostname": "pi.local", "serverIp": serverIp, "structureName": "carousel"},
    {"hostname": "pi1.local", "serverIp": serverIp, "structureName": "bench1"},
    {"hostname": "pi2.local", "serverIp": serverIp, "structureName": "bench2"}
]

config2 = {
    "Carousel": {"hostname": "pi.local",
                 "serverIp": serverIp},
    "Bench": {"hostname": "pi.local",
              "serverIp": serverIp}
}


def doSomethingHere():
    pass


# simple class that creates an SSH connection to a single computer.
class SSHConnection():
    def __init__(self, hostname, structureName, login, password):
        self.hostname = hostname
        self.structureName = structureName
        self.login = login
        self.password = password
        self.connectToSSH()

    # create an SSH connection, while passing errors if they arise.
    def connectToSSH(self):
        for x in range(10):
            try:
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(self.hostname, username=self.login, password=self.password)
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

    # once an SSH connection is created, then it is time to issue commands over the tubes
    def runCommand(self, commandToRun):
        stdin, stdout, stderr = self.ssh.exec_command(commandToRun)


# Now lets make multiple ssh connections to a list of computers
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
            # multiple threads because Gerald is a masochist
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


# Take a dictionary and parse out the correct string to send echo commands over the ssh connection
class echo:
    def __init__(self, fileName):
        self.fileName = fileName

    def writeConfig(self, configDict):
        keys = list(configDict.keys())

        configToWrite = []

        for index, key in enumerate(keys):
            if index == 0:
                string = """echo {"'%s'": "'%s'",  >> %s""" % (key, configDict[key], self.fileName)
            elif index == len(keys) - 1:
                string = """echo "'%s'": "'%s'"}  > %s""" % (key, configDict[key], self.fileName)
            else:
                string = """echo "'%s'": "'%s'",  > %s""" % (key, configDict[key], self.fileName)

            configToWrite.append(string)

        return configToWrite
