from multiSSH import MultiSSH


serverIp = "192.168.2.45"

config = {
    "Carousel": {"hostname": "pi1.local", "serverIp": serverIp},
    "Bench": {"hostname": "pi2.local", "serverIp": serverIp}
}

conn = MultiSSH(config)
conn.killSetupRestart()

