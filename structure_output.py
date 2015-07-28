#!/usr/bin/env python3
import sys

import util
import GPIO

if len(sys.argv) != 2:
    print("""Usage:
    structure_output.py <config_file>
""")
    sys.exit(1)

config = util.DreamlandConfig(sys.argv[1])
sub = util.SubClient(config.master(), config.topic())

outputs = GPIO.GPIO_outputs(config.output())

while True:
    action, level = sub.recv()
    outputs.output(action, int(level))
