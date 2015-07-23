#!/usr/bin/env python3
"""
Usage:
    structure_input.py <config_file>
"""
import sys

import docopt

args = docopt.docopt(__doc__)

import util
import GPIO

config = util.DreamlandConfig(args['<config_file>'])
pub = util.PubClient(config.master(), config.topic())

button = GPIO_button(config.input())

def pressed():
    pub.send(config.input['name'], GPIO.BUTTON_PRESSED)
    
def released():
    pub.send(config.input['name'], GPIO.BUTTON_RELEASED)
    
while True:
    button.wait(GPIO.BUTTON_PRESSED, pressed)
    button.wait(GPIO.BUTTON_RELEASED, released)
