import threading
import time


class SomeClass:
	def __init__(self, num):
		self.num = num
		self.func_to_be_threaded()

	def helloWorld(self):
		sentence = 'Hello World'
		while True:
			for word in sentence.split(' '):
				print(word + str(self.num))
				time.sleep(2)

	def func_to_be_threaded(self):
		threading.Thread(target=self.helloWorld).start()


if __name__ == '__main__':
	test = SomeClass(1)
	test2 = SomeClass(2)
	test3 = SomeClass(3)
	print(threading.activeCount())
