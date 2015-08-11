import RPi.GPIO as GPIO
 
gearsensor1_pin = 16
gearsensor2_pin = 18
gearsensor3_pin = 22


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gearsensor1b_pin, GPIO.IN)
    GPIO.setup(gearsensor2b_pin, GPIO.IN)
    GPIO.setup(gearsensor3b_pin, GPIO.IN)
    GPIO.setup(gearsensor1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(gearsensor2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(gearsensor3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

