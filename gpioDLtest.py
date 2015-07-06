import gpioDreamland as ioDL
import random
import time

ioDL.setmode()

relays = [7, 13, 11, 15]

for i, relay in enumerate(relays):
	relays[i] = ioDL.Relay(relay)

time.sleep(1)

for x in range(3):
	for relay in relays:
		relay.fireRelay(random.uniform(0.01, 0.5))
		time.sleep(random.uniform(0.01, 0.5))

ioDL.cleanup()
