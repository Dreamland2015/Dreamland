import RPi.GPIO as GPIO
import threading


class gpioOut(threading.Thread):
	def __init__(self, pinNum):
		threading.Thread.__init__(self)
		self.pinNum = pinNum

	def high(self):
		GPIO.output(self, self.pinNum, GPIO.HIGH)

	def low(self):
		GPIO.output(self, self.pinNum, GPIO.LOW)

	def cleanup(self):
		GPIO.cleanup()

	def run(self):
		GPIO.setmode(GPIO.board)
		GPIO.setup(self.pinNum, GPIO.OUT, GPIO.PUD_DOWN)


class gpioInput(threading.Thread):
	def __init__(self, pinNum):
		threading.Thread.__init__(self)
		self.pinNum = pinNum

	def high(self):
		GPIO.output(self, self.pinNum, GPIO.HIGH)

	def low(self):
		GPIO.output(self, self.pinNum, GPIO.LOW)

	def run(self):
		GPIO.setmode(GPIO.board)
		GPIO.setup(self.pinNum, GPIO.OUT, GPIO.PUD_DOWN)
