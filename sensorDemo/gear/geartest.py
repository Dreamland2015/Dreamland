import RPi.GPIO as GPIO
import time
import multiprocessing as mp
# from multiprocessing import Process as mp_Process, Array as mp_Array
from multiprocessing import Value as mp_Value, Lock as mp_Lock

# Count direction of gear teeth. Should be 1 or -1
COUNTDIR = 1

# number of teeth on gear. Should be 120 for Dreamland, 42 for demo gear.
NTEETH = 42

# Raspberry Pi pins to which the sensors are connected
gearsensor1_pin = 16
gearsensor2_pin = 18
gearsensor3_pin = 22

# The phase (measured in number of teeth) by which the rising edge of sensor 3
# precedes the rising edge sensor 1 in time, during "forward" rotation. Must be
# a number between 0 and 1.
# Should be close to 0.5 (equivalent to 180 degrees) if sensor 3 was positioned
# well. When it's 0.5, sensor 3 should see a gear tooth falling edge exactly when
# when sensor 1 sees a rising edge.
#sensor3_phase = 0.5
sensor3_phase = 0.125

# If use_sensor3 is True, it's used for more accurate speed and angle sensing
use_sensor3 = False
 
class gts_data(object):
    """ Class for gear tooth sensor data shared between processes """
    def __init__(self, angle=0, speed=0, tcount1=0, tcount2=0, tcount3=0):
        self.lock = mp.Lock()
        self.angle = mp.Value('d', angle)
        self.speed = mp.Value('d', speed)

        # gear tooth counts
        self.tcount1 = mp.Value('d', tcount1)
        self.tcount2 = mp.Value('d', tcount2)
        self.tcount3 = mp.Value('d', tcount3)
        
        # time since last tooth rising edge
        t = time.time()
        self.edge1time = mp.Value('d', t)
        self.edge2time = mp.Value('d', t)
        self.edge3time = mp.Value('d', t)
  
    def getdata(self, whichdata):
        with self.lock:
            if whichdata == 'angle': return self.angle.value
            elif whichdata == 'speed': return self.speed.value
            elif whichdata == 'tcount1': return self.tcount1.value
            elif whichdata == 'tcount2': return self.tcount2.value
            elif whichdata == 'tcount3': return self.tcount3.value
            elif whichdata == 'edge1time': return self.edge1time.value
            elif whichdata == 'edge2time': return self.edge2time.value
            elif whichdata == 'edge3time': return self.edge3time.value
            else: pass
 
    def setdata(self, whichdata, dat):
        with self.lock:
            if whichdata == 'angle': self.angle.value = dat
            elif whichdata == 'speed': self.speed.value = dat
            elif whichdata == 'tcount1': self.tcount1.value = dat
            elif whichdata == 'tcount2': self.tcount2.value = dat
            elif whichdata == 'tcount3': self.tcount3.value = dat
            elif whichdata == 'edge1time': self.edge1time.value = dat
            elif whichdata == 'edge2time': self.edge2time.value = dat
            elif whichdata == 'edge3time': self.edge3time.value = dat
            else: pass
 
def sensor_up(ch, sdat):
    """ 
    Callback function for a rising edge on a sensor. 
    
    Function that gets called by GPIO on a RPi channel rising edge. Counts
    gear teeth sensed by sensor 1 and 3. Sensor 2 is the quadrature sensor
    that determines whether sensor 1 and 3 teeth counted up or down.
    Assumes that sensor 3 is 180 degrees out of phase w.r.t sensor 1.
    
    Arguments:
    ch - the channels for sensor 1 or 3
    sdat - sensor data class 
    """

    sensor2 = GPIO.input(gearsensor2_pin)
    now = time.time()
    newtcount1 = newtcount3 = deltat1 = deltat3 = 0

    if (ch == gearsensor1_pin):
        # increment/decrement tooth counter
        step = COUNTDIR if (sensor2==0) else -COUNTDIR
        print(step)
        newtcount1 = sdat.getdata('tcount1') + step
        sdat.setdata('tcount1', newtcount1)

        if use_sensor3:
            # use sensor3 in addition to sensor1 for higher speed & angle resolution
            # time since last sensor 3 tooth edge
            deltat1 = now - sdat.getdata('edge3time')
            # speed: teeth/second * degrees/tooth / sensor3 phase advance
            speed = 1/deltat1 * 360/NTEETH / sensor3_phase
            toothfraction = -(sensor3_phase * step) % COUNTDIR    # magic formula to be fixed
            newangle = ((newtcount1+toothfraction) % NTEETH)* 360/NTEETH
        else:
            # time since last sensor 1 tooth edge
            deltat1 = now - sdat.getdata('edge1time')
            speed = 1/deltat1 * 360/NTEETH
            newangle = (newtcount1 % NTEETH)* 360/NTEETH

        sdat.setdata('angle', newangle)
        sdat.setdata('speed', speed)
        sdat.setdata('edge1time', now)
        speed1 = speed

    elif (ch == gearsensor3_pin):
        if use_sensor3:  # needs to be fixed
            step = -COUNTDIR if (sensor2==0) else COUNTDIR
            newtcount3 = sdat.getdata('tcount3') + step
            sdat.setdata('tcount3', newtcount3)
            deltat3 = now - sdat.getdata('edge3time')    # for debugging
            speed = 1/deltat3 * 360/NTEETH
            newangle = (newtcount1 % NTEETH)* 360/NTEETH
            sdat.setdata('edge3time', now)
            speed3 = speed
    else:
        return

    print("ch1: %d | %.5f sec    ch3: %d | %.5f sec"
               % (newtcount1, deltat1, newtcount3, deltat3) )

if __name__ == "__main__": 
    gtsdata = gts_data()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gearsensor1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(gearsensor2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(gearsensor3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(gearsensor1_pin, GPIO.RISING,
                          callback=lambda ch: sensor_up(ch, gtsdata))
    GPIO.add_event_detect(gearsensor3_pin, GPIO.RISING,
                          callback=lambda ch: sensor_up(ch, gtsdata))
 
    print("waiting for gear teeth")
    while True:
        try:
                curtime = time.time()
        except KeyboardInterrupt:
                GPIO.cleanup()
        time.sleep(5)
 
    GPIO.cleanup()
