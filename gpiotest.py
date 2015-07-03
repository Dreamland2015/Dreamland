import RPi.GPIO as GPIO
import time


class TimePerClick():
	def __init__(self, clickAccel, initalClickSpeed):
		self.clickAccel = clickAccel
		self.startTime = time.time()
		self.clickPerSec = initalClickSpeed

	def computeClickTime(self):
		currentTime = time.time()
		timeDiff = currentTime - self.startTime
		self.clickPerSec = self.clickPerSec - self.clickAccel * timeDiff
		dwell = 1 / self.clickPerSec * timeDiff

		return dwell


pins = [7, 11, 13, 15]
numLoops = 20

GPIO.setmode(GPIO.BOARD)

for pin in pins:
	GPIO.setup(pin, GPIO.OUT, GPIO.PUD_DOWN)

time.sleep(1)

timePerClick = TimePerClick(10, 100)


while timePerClick.clickPerSec > 0:
	for pin in pins:
		dwellTime = timePerClick.computeClickTime()
		GPIO.output(pin, GPIO.HIGH)
		print('high')
		time.sleep(dwellTime)
		GPIO.output(pin, GPIO.LOW)
		print('low')
		time.sleep(dwellTime)

GPIO.cleanup()
