import threading
import time


def setmode():
	print('GPIO layout set to board')


def cleanup():
	print('GPIO pins cleaned up')


class ThreadedGPIOOut(threading.Thread):
	def __init__(self, pinNum):
		threading.Thread.__init__(self)
		self.pinNum = pinNum
		self.setDaemon('True')
		self.start()

	def high(self):
		print('Pin ' + str(self.pinNum) + ' high')

	def low(self):
		print('Pin ' + str(self.pinNum) + ' low')

	def highForPeriod(self, timePeriod):
		self.high()
		print('sleeping for ' + str(timePeriod))
		time.sleep(timePeriod)
		self.low()

	def run(self):
		print('Setup pin # ' + str(self.pinNum) + ' as output')


class Poofer(ThreadedGPIOOut):
	def __init__(self, pinNum):
		self.pinNum = pinNum
		ThreadedGPIOOut.__init__(self, self.pinNum)

	def firePoofer(self, timePeriod):
		print('Firing relay on pin ' + str(self.pinNum) + ' for ' + str(self.timePeriod))
		self.highForPeriod(timePeriod)


# class PooferTimings(Relay):
# 	def __init__(self, ListOfPoofers):

def timingTest(listOfPoofers, durations):
	startTime = time.time()
	duration = 1
	for poofer in listOfPoofers:
		poofer.high()

	for index, poofer in enumerate(listOfPoofers):
		duration = durations[index]
		while time.time() - startTime < duration:
			pass
		poofer.low()
		timeElapsed = time.time() - startTime
		print(timeElapsed)

if __name__ == '__main__':
	pins = [1, 2, 3, 4]
	pins = [Poofer(pin) for pin in pins]
	timingTest(pins, [1, 2.2, 1, 4])
