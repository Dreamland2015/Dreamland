from multiSSH import MultiSSH


serverIp = '192.168.2.45'

config = {
    'carousel': {
        'hostname': "pi2.local",
        'inputPins': '1, 2',
        'outputPins': '7, 11, 13, 15',
        'serverIp': serverIp
    },
    "Bench": {
        'hostname': 'pi1.local',
        'inputPins': '1, 2',
        'outputPins': '3, 4',
        'serverIp': serverIp
    }
}

conn = MultiSSH(config)
conn.killSetupReboot()
