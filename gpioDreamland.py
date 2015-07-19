import RPi.GPIO as GPIO
import threading
import time


def setMode():
    GPIO.setmode(GPIO.BOARD)
    print('GPIO layout set to board')


def cleanup():
    GPIO.cleanup()
    print('GPIO pins cleaned up')


# Converts a string of a list '1,2,3,...,n' into a list of ints [1,2,3,....,n]
# used to convert the string of pins from the config file to use for gpio
def stringToList(stringOfInterest):
    return [int(s) for s in stringOfInterest.split(',')]


class ThreadedGPIOOut(threading.Thread):
    def __init__(self, pinNum):
        threading.Thread.__init__(self)
        self.pinNum = pinNum
        self.start()

    def high(self):
        GPIO.output(self.pinNum, GPIO.HIGH)

    def low(self):
        GPIO.output(self.pinNum, GPIO.LOW)

    def run(self):
        GPIO.setup(self.pinNum, GPIO.OUT, GPIO.PUD_DOWN)
        print('Setup pin # ' + str(self.pinNum) + ' as output')


class Poofer(ThreadedGPIOOut):
    def __init__(self, pinNum):
        self.pinNum = pinNum
        ThreadedGPIOOut.__init__(self, self.pinNum)
