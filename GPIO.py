import util

if util.running_on_pi():
    import Rpi.GPIO as _GPIO
    _GPIO.setmode(_GPIO.BOARD)
else:
    import fake_gpio as _GPIO

LOW = 0
HIGH = 1
BUTTON_PRESSED = 1
BUTTON_RELEASED = 0

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
            _GPIO.setup(pin_info['pin'], _GPIO.OUT)

    def output(self, name, level):
        _GPIO.output(self.cfg[name]['pin'], level)

class GPIO_button():
    def __init__(self, input_cfg):
        self.cfg = input_cfg
        self.pin = input_cfg['pin']
        _GPIO.setup(self.pin, _GPIO.IN)

    def wait(self, level, callback):
        _GPIO.wait_for_input(level)
        callback()
