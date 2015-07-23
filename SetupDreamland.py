#!/usr/bin/env python3
import time
import util

import multiSSH
from multiSSH import MultiSSH

serverIp = util.get_default_ip()

config = {
    'carousel-top': {
        'hostname': "samsonpi.local",
        'input': {'button':{'pin':1}},
        'output': {
            'flame1':{'pin':7},
            'flame2':{'pin':11},
            'flame3':{'pin':13},
            'center_flame':{'pin':15},
            },
        'master': serverIp,
    },
}

for structure_name, info in config.items():
    hostname = info['hostname']
    print('connecting to:', hostname, 'configuring as', structure_name)
    s = multiSSH.SSHConnection(hostname, structure_name)

    print('writing config for', hostname, 'info', info)
    s.write_structure_config(info)
    s.put_file('config/fcserver.json', '/etc/fcserver.json')

    git_cmd = 'git --git-dir /home/pi/repo/Dreamland/.git '
    s.runCommand(git_cmd + 'fetch')
    s.runCommand(git_cmd + 'reset --hard origin/master')

    def setup_supervisor():
        def put_supervisor_conf(filename):
            local_path = 'config/supervisor/'
            remote_path = '/etc/supervisor/conf.d/'
            s.put_file(local_path + filename, remote_path + filename)
        put_supervisor_conf('fcserver.conf')
        put_supervisor_conf('structure_input.conf')
        put_supervisor_conf('structure_output.conf')

    setup_supervisor()
    s.runCommand('sudo supervisorctl reload')
