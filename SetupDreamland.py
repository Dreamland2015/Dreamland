#!/usr/bin/env python3
import time
import util

import multiSSH

serverIp = util.get_default_ip()

configs = [
    { 'topic': 'carousel-top',
      'hostname': "pi15.local",
      'input': {'button':{'pin':1}},
      'output': {
          'flame1':{'pin':6},
          'flame2':{'pin':13},
          'flame3':{'pin':19},
          'center_flame':{'pin':26},
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
    {
        'topic': 'lantern1',
        'hostname': "pi8.local",
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
        'topic': 'carousel-top',
        'hostname': "pi15.local",
        'input': {'button':{'pin':7}},
        'output': { },
        'master': serverIp,
    },
    {
        'topic': 'outerbench1',
        'hostname': "pi7.local",
        'master': serverIp,
    },
    {
        'topic': 'lantern1',
        'hostname': "pi9.local",
        'master': serverIp,
    },
]

s = multiSSH.MultiDreamandPi([configs[-1]], debug=True)
s.do_full_setup()
#s.do_partial_setup()
print('Pi is now fully setup')
