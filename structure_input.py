#!/usr/bin/env python3
import sys

import util
import GPIO

if len(sys.argv) != 2:
    print("""Usage:
    structure_input.py <config_file>
""")
    sys.exit(1)

config = util.DreamlandConfig(sys.argv[1])
pub = util.PubClient(config.master(), config.topic())

input_info = list(config.input().items())[0]
name = input_info[0]
button = GPIO.GPIO_button(input_info[1])

def pressed():
    pub.send(name, GPIO.BUTTON_PRESSED)
    
def released():
    pub.send(name, GPIO.BUTTON_RELEASED)
    
while True:
    button.wait(GPIO.BUTTON_PRESSED, pressed)
    button.wait(GPIO.BUTTON_RELEASED, released)
