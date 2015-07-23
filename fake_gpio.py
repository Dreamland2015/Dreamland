IN = 0
OUT = 1

def setup(pin, in_out):
    print("GPIO CONFIG pin", pin, "configured for", ['input','output'][in_out])

def output(pin, level):
    print("GPIO pin", pin, "set", ['low','high'][level])

def cleanup():
    print("GPIO CLEANUP")
