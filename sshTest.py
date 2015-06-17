import sys
import time
import paramiko
import multiprocessing as mp

# Configure SSH information
login = 'pi'
password = 'raspberry'
config = [
    {'name': 'carousel', 'hostname': 'pi.local'},
    {'name': 'bench', 'hostname': 'pi1.local'},
    {'name': 'bench1', 'hostname': 'pi2.local'}
]

# server
serverIp = '10.0.1.165'


class Dreamlandia():
    def __init__(self, dreamlandObjects):
        for index, dreamlandObject in enumerate(dreamlandObjects):
            self.structureName = dreamlandObject['name']
            self.host = dreamlandObject['hostname']
            pool = mp.Pool(processes=len(config))
            results = [pool.apply_async(self.connectToServer, args=()) for dreamlandObject in config]
            output = [p.get() for p in results]

    def connectToServer(self):
        i = 1
        while True:
            try:
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(self.host, username=login, password=password)
                print ("Connected to " + self.structureName)
                self.startStructure()
                break
            except paramiko.AuthenticationException:
                print ("Authentication failed when connecting to " + self.structureName)
                sys.exit(1)
            except:
                print ("Could not SSH to " + self.structureName + ", waiting for it to start")
                i += 1
                time.sleep(1)

            # If we could not connect within time limit
            if i == 30:
                print ("Could not connect to " + self.structureName + ". Giving up")
                sys.exit(1)

    def startStructure(self):
        stdin, stdout, stderr = self.ssh.exec_command("python3 /home/pi/repo/Dreamland/DreamlandDemo/python/dreamlandStructure.py" + self.structureName + ' ' + serverIp)


if __name__ == '__main__':
    Dreamlandia(config)
