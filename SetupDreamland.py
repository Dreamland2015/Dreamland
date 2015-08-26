#!/usr/bin/env python3
# import time
import util

import multiSSH

serverIp = util.get_default_ip()
# serverIp = "192.168.2.5"

configs = [
    # {
    #     'topic': 'carousel-top',
    #     'hostname': "pi15.local",
    #     'input': {'button': {'pin': 1}},
    #     'output': {
    #         'flame1': {'pin': 6},
    #         'flame2': {'pin': 13},
    #         'flame3': {'pin': 19},
    #         'center_flame': {'pin': 26}},
    #     'master': serverIp,
    # },
    # {
    #     'topic': 'carouselBottom',
    #     'hostname': "192.168.2.55",
    #     'master': serverIp,
    # },
    # {
    #     'topic': 'center',
    #     'hostname': 'pi10.local',
    #     'master': serverIp,
    # },
    {
        'topic': 'lampPost1',
        'hostname': "pi16.local",
        'input': {'button': {'pin': 12}},
        'output': {
                    'flame': {'pin': 11}},
        'master': serverIp,
    },
    {
        'topic': 'lampPost2',
        'hostname': "pi8.local",
        'input': {'button': {'pin': 12}},
        'output': {
                    'flame': {'pin': 11}},
        'master': serverIp,
    },
    # {
    #     'topic': 'lampPost3',
    #     'hostname': "pi4.local",
    #     'input': {'button': {'pin': 12}},
    #     'output': {
    #                 'flame': {'pin': 11}},
    #     'master': serverIp,
    # },
    # {
    #     'topic': 'outerbench1',
    #     'hostname': "192.168.2.57",
    #     'master': serverIp,
    # },
    # {
    #     'topic': 'outerbench2',
    #     'hostname': "pi6.local",
    #     'master': serverIp,
    # },
    # {
    #     'topic': 'outerbench3',
    #     'hostname': "pi5.local",
    #     'master': serverIp,
    # }
]

s = multiSSH.MultiDreamandPi(configs, debug=True)
# s = multiSSH.MultiDreamandPi([configs[1]], debug=True)
# s.do_full_setup()
s.do_partial_setup()
print('Pi is now fully setup')
