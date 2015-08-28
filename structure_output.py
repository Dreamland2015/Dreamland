#!/usr/bin/env python3
import sys
import traceback

import util
import pi_gpio as GPIO

if len(sys.argv) != 2:
    print("""Usage:
    structure_output.py <config_file>
""")
    sys.exit(1)

config = util.DreamlandConfig(sys.argv[1])
sub = util.SubClient(config.master(), config.topic())

outputs = GPIO.GPIO_outputs(config.output())

print(config.config)

while True:
    action, level = sub.recv()
    print("action", action, level)
    try:
        outputs.output(action, int(level))
    except KeyError:
        traceback.print_exc()
