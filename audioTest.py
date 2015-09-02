import os
import util

serverIp = '192.168.2.5'

sub = util.SubClient(serverIp, 'motion')

maxSpeed = 25	# [RPM]
breakOverSpeed = 20 # [RPM]
initialVolume = 85
maximumVolume = 100
minimumVolume = 20



def changeSysVolumeDown(carouselSpeed, maxSpeed, maxVolume, changeSpeed):
	volume = ((minimumVolume - maximumVolume) / (maxSpeed - changeSpeed)) * (carouselSpeed - changeSpeed) + maximumVolume
	sendString = 'amixer -D pulse sset Master ' + str(volume) + '%'
	os.system(sendString)

def changeSysVolumeUp(carouselSpeed, maxSpeed, initVolume, changeSpeed):
	volume = ((maximumVolume - initialVolume) / (changeSpeed)) * (carouselSpeed) + initialVolume
	sendString = 'amixer -D pulse sset Master ' + str(volume) + '%'
	os.system(sendString)

while True:
	angle, velocity = sub.recv()[0].split(",") # [deg], [deg/s]
	print(velocity)
	carouselSpeed = float(velocity) * 60 / 360
	# carouselSpeed = float(velocity)
	carouselSpeed = abs(carouselSpeed)

	print(velocity)

	if 0 < carouselSpeed < breakOverSpeed:
		changeSysVolumeUp(carouselSpeed, maxSpeed, initialVolume, breakOverSpeed)
	elif carouselSpeed < maxSpeed:
		changeSysVolumeDown(carouselSpeed, maxSpeed, maximumVolume, breakOverSpeed)

