import os
import tempfile
import threading
import time
import socket
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
    def __init__(self, hostname, debug=None):
        self.hostname = hostname
        self.debug = debug
        self.ip = None
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
                self.ip = socket.gethostbyname(self.hostname)
                print ("Connected to " + self.hostname)
                return
            except (paramiko.ssh_exception.AuthenticationException, paramiko.AuthenticationException):
                print ("Authentication failed when connecting to " + self.hostname)
                sys.exit(1)
            except OSError:
                print("Encountered OSError on connection to", self.hostname, "No route to host expected")
                import traceback
                traceback.print_exc()

                print ("Could not SSH to " + self.hostname + ", waiting for it to start")
                time.sleep(1)
                continue

        # If no connection in the allowed time.
        raise RuntimeError("Could not connect to " + self.hostname + ". Giving up")

    # once an SSH connection is created, then it is time to issue commands over the tubes
    def runCommand(self, commandToRun):
        stdin, stdout, stderr = self.ssh.exec_command(commandToRun)
        stdout.channel.exit_status_ready()

        if self.debug:
            print('Running:\n\t', commandToRun, 'on', self.hostname, 'at', self.ip)
            while not stdout.channel.exit_status_ready():
                print(str(stdout.channel.recv(1024), encoding='utf-8'), end="")

        rval = stdout.channel.recv_exit_status()
        if rval != 0:
            print("Error running cmd:", commandToRun)
        return rval

    def tryCommand(self, commandToRun):
        rval = self.runCommand(commandToRun)
        if rval != 0:
            raise Exception("Failure running %s" % (commandToRun, ))
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


class DreamlandPi(SSHConnection):
    def __init__(self, config, debug=None):
        self.config = config
        self.hostname = config['hostname']
        self.topic = config['topic']
        super(DreamlandPi, self).__init__(self.hostname, debug)

    def supervisor_reload(self):
        """ This restarts the entire supervisor daemon. """
        self.runCommand('sudo supervisorctl reload')

    def supervisor_reread(self):
        """ This just rereads all the config files. """
        self.runCommand('sudo supervisorctl reread')

    def setup_rc_local(self):
        """
        Overwrite rc.local with ours.

        The one on the image sets up fcserver to run from there, which makes it
        hard to restart to load a new config file.
        """
        self.put_file('config/rc.local', '/etc/rc.local')
        self.runCommand('sudo killall fcserver')
        print('rc.local restored.')

    def setup_apt(self):
        """
        Dreamland Master is configured as an apt mirror, so set up apt on the
        Pi's to use the local mirror.
        """
        self.put_file('config/apt.sources.list', '/etc/apt/sources.list')
        self.runCommand('sudo rm /etc/apt/sources.list.d/collabora.list')
        self.runCommand('sudo rm /etc/apt/sources.list.d/raspi.list')
        self.runCommand('sudo apt-get update')
        self.runCommand('sudo apt-get -y upgrade')
        print('Apt configured to use local repo.')

    def setup_supervisor(self):
        """
        Install supervisor and copy config files for it.
        """
        self.runCommand('sudo apt-get install -y supervisor')
        def put_supervisor_conf(filename):
            local_path = 'config/supervisor/'
            remote_path = '/etc/supervisor/conf.d/'
            self.put_file(local_path + filename, remote_path + filename)
        put_supervisor_conf('fcserver.conf')
        put_supervisor_conf('structure_input.conf')
        put_supervisor_conf('structure_output.conf')
        self.supervisor_reread()
        print('Supervisor configured and reloaded on', self.hostname)

    def setup_fadecandy(self):
        """
        Fadecandy server config
        """
        self.put_file('config/fcserver.json', '/etc/fcserver.json')
        self.runCommand('sudo rm /usr/local/bin/fcserver.json')
        self.runCommand('sudo killall fcserver')
        self.supervisor_reread()

    def do_full_setup(self):
        self.setup_rc_local()
        self.setup_apt()
        self.setup_supervisor()
        self.setup_fadecandy()
        self.supervisor_reload()

    def do_code_refresh(self):
        for filename in [x for x in os.listdir('.') if x[-3:] == '.py']:
            self.put_file(filename, '/home/pi/repo/Dreamland/%s' % (filename, ))
        self.write_structure_config(self.config)
        self.supervisor_reload()

    def do_partial_setup(self):
        self.do_code_refresh()
        self.supervisor_reload()

class MultiDreamandPi:
    def __init__(self, configs, debug=False):
        self.configs = configs
        self.sshes = {}
        for config in self.configs:
            hostname = config['hostname']
            structure_name = config['topic']
            #print.
            s = DreamlandPi(config, debug=debug)
            print('s', type(s), s)
            self.sshes[structure_name] = (hostname, structure_name, s)

    def _do_on_all(self, fn):
        threads = []
        for x in self.sshes.values():
            #fn(x)
            t = threading.Thread(target=lambda: fn(x), daemon=True)
            t.start()
            threads.append(t)
        for host, structure_name, t in threads:
            t.join()
            print("Finisehd run for", structure_name, "at", host)

    def do_full_setup(self):
        self._do_on_all(DreamlandPi.do_full_setup)

    def do_partial_setup(self):
        self._do_on_all(DreamlandPi.do_partial_setup)

    def do_code_refresh(self):
        self._do_on_all(DreamlandPi.do_code_refresh)

    def supervisor_reload(self):
        self._do_on_all(DreamlandPi.supervisor_reload)
