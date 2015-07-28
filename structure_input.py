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

button = GPIO.GPIO_button(config.input())

def pressed():
    pub.send(config.input()['name'], GPIO.BUTTON_PRESSED)
    
def released():
    pub.send(config.input()['name'], GPIO.BUTTON_RELEASED)
    
while True:
    button.wait(GPIO.BUTTON_PRESSED, pressed)
    button.wait(GPIO.BUTTON_RELEASED, released)
