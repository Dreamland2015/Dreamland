from gpioDreamland import gpioOut
import time

pins = [7, 13, 11, 15]

pins = [gpioOut(pin) for pin in pins]

time.sleep(1)

for x in range(3):
	for pin in pins:
		pin.high()
		time.sleep(1)
		pin.low()
		time.sleep(1)

[pin.cleanup() for pin in pins]
