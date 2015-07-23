import tempfile
import threading
import time
import sys

from contextlib import contextmanager

import paramiko

#####################################################################################################################################
#####################################################################################################################################
# This file creates several classes used in the management of Dreamland 2015, which are the following:

# - SSHConnection handles all of the details establishing a SSH connection to a single host, as well as issuing commands to the host
# - MultiSSH expands SSHConnection by creating a list of SSHConnection objects and passing them commands
# - Echo is frankly rather hacky, but it allows for the creation of the structureConfig.py on each RPI,
#   this allows the dreamlandStructure.py scripts to pull the serverIp, that structures name and the structures hostname

#####################################################################################################################################
#####################################################################################################################################


# Raspberry Pi login information
login = "pi"
password = "raspberry"

# Comand to run dreamlandStructure.py on RPI's
startDreamlandStructure = "sudo python3 ~/repo/Dreamland/dreamlandStructure.py"


#####################################################################################################################################
# simple class that creates an SSH connection to a single computer.
#####################################################################################################################################
class SSHConnection():
    def __init__(self, hostname, structureName):
        self.hostname = hostname
        self.structureName = structureName
        self.connect()

    # create an SSH connection, while passing errors if they arise.
    def connect(self):
        for x in range(10):
            try:
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(self.hostname, username=login, password=password)

                self.transport = self.ssh.get_transport()
                self.sftp = paramiko.SFTPClient.from_transport(self.transport)
                print ("Connected to " + self.structureName)
                return
            except (paramiko.ssh_exception.AuthenticationException, paramiko.AuthenticationException):
                print ("Authentication failed when connecting to " + self.structureName)
                sys.exit(1)
            except OSError:
                print("Encountered OSError on connection to", self.hostname, "No route to host expected")
                import traceback
                traceback.print_exc()

                print ("Could not SSH to " + self.structureName + ", waiting for it to start")
                time.sleep(1)
                continue

        # If no connection in the allowed time.
        raise RuntimeError("Could not connect to " + self.structureName + ". Giving up")

    # once an SSH connection is created, then it is time to issue commands over the tubes
    def runCommand(self, commandToRun):
        stdin, stdout, stderr = self.ssh.exec_command(commandToRun)
        stdout.channel.exit_status_ready()

        rval = stdout.channel.recv_exit_status()
        if rval != 0:
            print("Error running cmd:", commandToRun)
        return rval

    # take a list of commands and send those over SSH
    def runMultipleCommands(self, commandList):
        for string in commandList:
            self.runCommand(string)
            print(string)
            time.sleep(0.5)

    @contextmanager
    def using_temp_filename(self, remote_destination_filename):
        tempfilename = tempfile.mktemp()
        yield tempfilename
        self.sudo_write_file(tempfilename, remote_destination_filename)

    # Ghetto-rig the file writer to have root perms.
    def sudo_write_file(self, src, dest):
        self.runCommand('sudo mv "%s" "%s"' % (src, dest))

    # Copy a file to the SSH server
    def put_file(self, local_filename, remote_filename):
        with self.using_temp_filename(remote_filename) as tempfilename:
            self.sftp.put(local_filename, tempfilename)

    # Write a string to the SSH server
    def write_file(self, remote_filename, contents):
        with self.using_temp_filename(remote_filename) as tempfilename:
            with self.sftp.open(tempfilename, 'w') as f:
                f.write(contents)

    def write_structure_config(self, config):
        with self.using_temp_filename('/etc/dreamland.py') as tempfilename:
            self.write_file(tempfilename, 'config='+str(config)+'\n')

#####################################################################################################################################
# Now lets make multiple ssh connections and store those in a list
#####################################################################################################################################
class MultiSSH:
    def __init__(self, configDict):
        self.configDict = configDict
        self.structureNames = list(self.configDict.keys())
        self.sshConnections = []
        for structure in self.structureNames:
            self.sshConnections.append(SSHConnection(self.configDict[structure]["hostname"], structure))

    # Run a single command on all SSH connections
    def runOnAll(self, commandToRun):
        for connection in self.sshConnections:
            connection.runCommand(commandToRun)

    # Run a list of commands on all SSH connections
    def runMultipleCommandsOnAll(self, commandList):
        for string in commandList:
            self.runOnAll(string)

    # Kill python scripts running on each connection
    def killAllPythonScripts(self):
        self.runOnAll("sudo pkill python")

    # Restart the python script for each structure
    def restartDreamlandStructureScript(self):
        self.runOnAll(startDreamlandStructure)
        print('restarting ' + self.str)

    def rebootRaspberryPis(self):
        print('Rebooting RPIs')
        self.runOnAll('sudo reboot')

    # For the entire piece, kill python scripts, reset config files and restart the piece
    def killSetupReboot(self):
        self.killAllPythonScripts()
        time.sleep(0.5)
        self.setupConfigFile()
        time.sleep(0.5)
        self.rebootRaspberryPis()

    # Create a configuration file on the appropriate strucutre RPI
    def setupConfigFile(self):
        configName = "structureConfig"
        for connection in self.sshConnections:
            name = connection.structureName
            print('Setting up configuration file on ' + name)
            e = echo(configName, self.configDict[name], name)
            commandsToWrite = e.writeConfig()
            connection.runMultipleCommands(commandsToWrite)


#####################################################################################################################################
# Take a dictionary and parse out the correct string to send echo commands over the ssh connection
#####################################################################################################################################
class ConfigWriter:
    def __init__(self, fileName, configDict, name):
        self.fileName = fileName
        self.configDict = configDict
        self.structureName = name

    def writeConfig(self):
        file_location = '/etc/dreamland.py'

        open(file_location,'w').write(str(self.configDict))
        return configToWrite
