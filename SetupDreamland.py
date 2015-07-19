from multiSSH import MultiSSH
import time


serverIp = '192.168.2.45'

config = {
    'pi2': {
        'hostname': "pi2.local",
        'inputPins': '1, 2',
        'outputPins': '7, 11, 13, 15',
        'serverIp': serverIp
    },
    "pi1": {
        'hostname': 'pi1.local',
        'inputPins': '1, 2',
        'outputPins': '3, 4',
        'serverIp': serverIp
    },
    "pi3": {
        'hostname': 'pi3.local',
        'inputPins': '1, 2',
        'outputPins': '3, 4',
        'serverIp': serverIp
    },
    "pi4": {
        'hostname': 'pi4.local',
        'inputPins': '1, 2',
        'outputPins': '3, 4',
        'serverIp': serverIp
    },
    "pi5": {
        'hostname': 'pi5.local',
        'inputPins': '1, 2',
        'outputPins': '3, 4',
        'serverIp': serverIp
    },
    "pi6": {
        'hostname': 'pi6.local',
        'inputPins': '1, 2',
        'outputPins': '3, 4',
        'serverIp': serverIp
    }
}

conn = MultiSSH(config)
conn.killSetupReboot()
