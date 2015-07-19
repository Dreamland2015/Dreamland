import threading


def setMode():
    print('GPIO layout set to board')


def cleanup():
    print('GPIO pins cleaned up')


# Converts a string of a list '1,2,3,...,n' into a list of ints [1,2,3,....,n]
# used to convert the string of pins from the config file to use for gpio
def stringToList(stringOfInterest):
    print('Converted pins: ' + stringOfInterest)
    return [int(s) for s in stringOfInterest.split(',')]


class ThreadedGPIOOut(threading.Thread):
    def __init__(self, pinNum):
        threading.Thread.__init__(self)
        self.pinNum = pinNum
        # self.setDaemon('True')
        self.start()

    def high(self):
        print('Pin ' + str(self.pinNum) + ' high')

    def low(self):
        print('Pin ' + str(self.pinNum) + ' low')

    def run(self):
        print('Setup pin # ' + str(self.pinNum) + ' as output')


class Poofer(ThreadedGPIOOut):
    def __init__(self, pinNum):
        self.pinNum = pinNum
        ThreadedGPIOOut.__init__(self, self.pinNum)
