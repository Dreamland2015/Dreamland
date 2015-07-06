import RPi.GPIO as GPIO
import threading
import time


def setmode():
	GPIO.setmode(GPIO.BOARD)
	print('GPIO layout set to board')


def cleanup():
	GPIO.cleanup()
	print('GPIO pins cleaned up')


class ThreadedGPIOOut(threading.Thread):
	def __init__(self, pinNum):
		threading.Thread.__init__(self)
		self.pinNum = pinNum
		self.start()

	def high(self):
		GPIO.output(self.pinNum, GPIO.HIGH)

	def low(self):
		GPIO.output(self.pinNum, GPIO.LOW)

	def highForPeriod(self, timePeriod):
		self.high()
		time.sleep(timePeriod)
		self.low()

	def run(self):
		GPIO.setup(self.pinNum, GPIO.OUT, GPIO.PUD_DOWN)
		print('Setup pin # ' + str(self.pinNum) + ' as output')


class Relay(ThreadedGPIOOut):
	def __init__(self, pinNum):
		self.pinNum = pinNum
		ThreadedGPIOOut.__init__(self, self.pinNum)

	def fireRelay(self, timePeriod):
		self.highForPeriod(timePeriod)
