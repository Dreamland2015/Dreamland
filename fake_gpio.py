import time

IN = 0
OUT = 1

PUD_UP = 0 # Pullup enable

RISING = 1
FALLING = 0

def setup(pin, in_out, pull_up_down=None):
    print("GPIO CONFIG pin", pin, "configured for", ['input','output'][in_out])
    if pull_up_down:
        print("  UP DOWN SET:", pull_up_down)

def output(pin, level):
    print("GPIO pin", pin, "set", ['low','high'][level])

def cleanup():
    print("GPIO CLEANUP")

def wait_for_input(level):
    print("GPIO fake input wait, sleeping...", end = "")
    time.sleep(4)
    print("GPIO fake input wait returning.")
