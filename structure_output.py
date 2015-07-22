#!/usr/bin/env python3
"""
Usage:
    structure_output.py <config_file>
"""
import sys

import docopt

args = docopt.docopt(__doc__)

import util
import GPIO

config = util.DreamlandConfig(args['<config_file>'])
sub = util.SubClient(config.master(), config.topic())

outputs = GPIO.GPIO_outputs(config.output())

while True:
    action, level = sub.recv()
    outputs.output(action, int(level))
