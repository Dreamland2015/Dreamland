#!/usr/bin/env python3
import time
import util

import multiSSH
from multiSSH import MultiSSH

serverIp = util.get_default_ip()

config = {
#    'carousel-top': {
#        'hostname': "samsonpi.local",
#        'input': {'button':{'pin':1}},
#        'output': {
#            'flame1':{'pin':7},
#            'flame2':{'pin':11},
#            'flame3':{'pin':13},
#            'center_flame':{'pin':15},
#            },
#        'master': serverIp,
#    },
    'carousel': {
        'topic': 'carousel',
        'hostname': "pi7.local",
        'input': {'button':{'pin':7}},
        'output': { },
            #'flame1':{'pin':7},
            #'flame2':{'pin':11},
            #'flame3':{'pin':13},
            #'center_flame':{'pin':15},
            #},
        'master': serverIp,
    },
}

for structure_name, info in config.items():
    hostname = info['hostname']
    print('connecting to:', hostname, 'configuring as', structure_name)
    s = multiSSH.SSHConnection(hostname, structure_name, debug=True)

    #s.put_file('config/apt.sources.list', '/etc/apt/sources.list')
    #s.runCommand('sudo mv /etc/apt/sources.list.d/collabora.list /etc/apt/sources.not.collabora.list')
    #s.runCommand('sudo mv /etc/apt/sources.list.d/raspi.list /etc/apt/sources.not.raspi.list')

    #s.runCommand('sudo apt-get update')
    #s.runCommand('sudo apt-get install -y supervisor')

    #print('Writing config for', hostname, 'info', info)
    print('Writing config for', hostname)
    s.write_structure_config(info)
    s.put_file('config/fcserver.json', '/etc/fcserver.json')

    #git_cmd = 'git --git-dir /home/pi/repo/Dreamland/.git '
    #s.runCommand(git_cmd + 'fetch')
    ##s.runCommand(git_cmd + 'reset --hard origin/samson-zmq-xpub-xsub')
    #s.runCommand(git_cmd + 'reset --hard HEAD')
    #s.runCommand(git_cmd + 'checkout origin/samson-zmq-xpub-xsub')
    repo_cmd = 'cd /home/pi/repo/Dreamland/; git '

    s.runCommand(repo_cmd + 'fetch')
    s.runCommand(repo_cmd + 'reset --hard HEAD')
    s.runCommand(repo_cmd + 'checkout -f origin/samson-zmq-xpub-xsub')

    def setup_supervisor():
        def put_supervisor_conf(filename):
            local_path = 'config/supervisor/'
            remote_path = '/etc/supervisor/conf.d/'
            s.put_file(local_path + filename, remote_path + filename)
        put_supervisor_conf('fcserver.conf')
        put_supervisor_conf('structure_input.conf')
        put_supervisor_conf('structure_output.conf')
        s.runCommand('sudo supervisorctl reload')
        print('Supervisor reloaded on', hostname)

    setup_supervisor()

    s.runCommand('sudo mv /etc/rc.local /etc/rc.local.fcserver')

    s.put_file('config/rc.local', '/etc/rc.local.set_ip')

    s.runCommand('sudo rm /etc/rc.local')
    s.runCommand('sudo ln -s /etc/rc.localset_ip /etc/rc.local')
