import sys
import time
import paramiko
import multiprocessing as mp

config = [
    {'hostname': 'pi.local', 'name': 'carousel'},
    {'hostname': 'pi.local', 'name': 'bench'}
]

login = 'pi'
password = 'raspberry'


class Dreamlandia():
    # def __init__(self):
    #     for host in hostnames:
    #         p = mp.Process(target=self.connectToServer(host))
    #     p.start()
    #     p.join()
    def __init__(self):
        pool = mp.Pool(processes=12)
        results = [pool.apply_async(self.connectToServer, args=(dreamlandObject,)) for dreamlandObject in config]
        output = [p.get() for p in results]

    def connectToServer(self, dreamlandObject):
        host = dreamlandObject['hostname']
        structureName = dreamlandObject['name']
        i = 1
        while True:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username=login, password=password)
                print ("Connected to " + structureName)
                break
            except paramiko.AuthenticationException:
                print ("Authentication failed when connecting to " + structureName)
                sys.exit(1)
            except:
                print ("Could not SSH to " + structureName + ", waiting for it to start")
                i += 1
                time.sleep(1)

            # If we could not connect within time limit
            if i == 30:
                print ("Could not connect to " + structureName + ". Giving up")
                sys.exit(1)

    # stdin, stdout, stderr = ssh.exec_command("python3 /home/pi/repo/Dreamland/DreamlandDemo/python/dreamlandStructure.py bench1 10.0.1.165")


if __name__ == '__main__':
    Dreamlandia()
