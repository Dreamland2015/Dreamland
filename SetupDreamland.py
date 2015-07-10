from multiSSH import MultiSSH


serverIp = '10.0.1.165'

config = {
    'Carousel': {
        'hostname': "pi1.local",
        'inputPins': '1, 2',
        'outputPins': '3, 4',
        'serverIp': serverIp
    },
    "Bench": {
        'hostname': 'pi2.local',
        'inputPins': '1, 2',
        'outputPins': '3, 4',
        'serverIp': serverIp
    }
}

conn = MultiSSH(config)
conn.setupConfigFile()
