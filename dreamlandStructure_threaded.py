r1 = Subscriber('localhost', '2345', 'carousel', False)
r2 = Subscriber('localhost', '2345', 'bench_1', False)
r3 = Subscriber('localhost', '2345', 'bench_2', False)
s1 = Publisher('localhost', '2345', True)
time.sleep(2)
for thread in threading.enumerate():
	print(thread)

# for x in range(1):
# 	message = input()
# 	topic, message = message.split(',')
# 	print(message)
# 	s1.sendMessage(topic, message)

s1.sendMessageToMultiple(['carousel', 'bench_1', 'bench_2'], 'Hello World')