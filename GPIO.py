import time

import util

if util.running_on_pi():
    import RPi.GPIO as _GPIO
    _GPIO.setmode(_GPIO.BOARD)
else:
    import fake_gpio as _GPIO

LOW = 0
HIGH = 1
BUTTON_PRESSED = _GPIO.FALLING
BUTTON_RELEASED = _GPIO.RISING

cleanup = _GPIO.cleanup

class GPIO_outputs():
    """
    config is a python dict that looks like:

        {'pin name': {'pin': board-relative pin number}}

    eg:

        {'center':{'pin':1}}
    """
    def __init__(self, output_cfg):
        self.cfg = output_cfg
        for name, pin_info in output_cfg.items():
            print("Setting up", name, 'output')
            _GPIO.setup(pin_info['pin'], _GPIO.OUT)

    def output(self, name, level):
        _GPIO.output(self.cfg[name]['pin'], level)

class GPIO_button():
    def __init__(self, input_cfg):
        self.cfg = input_cfg
        self.pin = input_cfg['pin']
        _GPIO.setup(self.pin, _GPIO.IN, pull_up_down=_GPIO.PUD_UP)

    def wait(self, level, callback):
        _GPIO.wait_for_edge(self.pin, level)
        callback()
        time.sleep(.01)
