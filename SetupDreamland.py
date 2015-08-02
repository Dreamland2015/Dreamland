#!/usr/bin/env python3
import time
import util

import multiSSH
from multiSSH import MultiSSH

serverIp = util.get_default_ip()

configs = [
    { 'topic': 'carousel-top',
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
    {
        'topic': 'carousel',
        'hostname': "pi1.local",
        'input': {'button':{'pin':7}},
        'output': { },
            #'flame1':{'pin':7},
            #'flame2':{'pin':11},
            #'flame3':{'pin':13},
            #'center_flame':{'pin':15},
            #},
        'master': serverIp,
    },
    {
        'topic': 'carousel',
        'hostname': "samsonpi.local",
        'input': {'button':{'pin':7}},
        'output': { },
            #'flame1':{'pin':7},
            #'flame2':{'pin':11},
            #'flame3':{'pin':13},
            #'center_flame':{'pin':15},
            #},
        'master': serverIp,
    },
]

s = multiSSH.MultiDreamandPi([configs[2]])
s.do_full_setup()
#s.do_partial_setup()
print('Pi is now fully setup')
