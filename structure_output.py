import util
import GPIO

config = util.read_config()
sub = util.SubClient(config['master'], config['topic'])

while True:
    action, level = sub.recv()
    try:
        GPIO.set(config[action], level)
    except KeyError:
        import traceback
        traceback.print_exc()
        err_msg = "Error on %s trying to set %s to %s" % (config['topic'], action, level)
        pub = util.PubClient(config['master'], 'error').send(err_msg)
