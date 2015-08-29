import RPi.GPIO as GPIO
import util
import time
import multiprocessing as mp
# from multiprocessing import Process as mp_Process, Array as mp_Array
from multiprocessing import Value as mp_Value, Lock as mp_Lock

# Count direction of gear teeth. Should be 1 or -1
COUNTDIR = 1
# If we're only counting the tooth rising edges, set this to False
USEFALLINGEDGE = True

# number of teeth on gear. Should be 120 for Dreamland, 42 for demo gear.
#NTEETH = 42
NTEETH = 120

# Raspberry Pi pins to which the sensors are connected
# Each sensor is connected to two pins. The first is pullup, and senses rising edges. The
# second is floating, and senses falling edges.
gearsensor1_pin = 16
gearsensor2_pin = 18
gearsensor3_pin = 22
gearsensor1b_pin = 15
gearsensor2b_pin = 19
gearsensor3b_pin = 21

# The phase (measured in number of teeth) by which the rising edge of sensor 3
# precedes the rising edge sensor 1 in time, during "forward" rotation. Must be
# a number between 0 and 1.
# Should be close to 0.5 (equivalent to 180 degrees) if sensor 3 was positioned
# well. When it's 0.5, sensor 3 should see a gear tooth falling edge exactly when
# when sensor 1 sees a rising edge. Value is not too critical if sensor 3 is
# not used...
sensor3_phase = 0.5
#sensor3_phase = 0.125

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
        self.edge1btime = mp.Value('d', t)
        self.edge2btime = mp.Value('d', t)
        self.edge3btime = mp.Value('d', t)

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
            elif whichdata == 'edge1btime': return self.edge1btime.value
            elif whichdata == 'edge2btime': return self.edge2btime.value
            elif whichdata == 'edge3btime': return self.edge3btime.value
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
            elif whichdata == 'edge1btime': self.edge1btime.value = dat
            elif whichdata == 'edge2btime': self.edge2btime.value = dat
            elif whichdata == 'edge3btime': self.edge3btime.value = dat
            else: pass

    def position_reset(self)
       self.setdata(angle, 0)    

def sensor_edge(ch, sdat, edgetype):
    """ 
    Callback function for a rising edge on a sensor. 

    Function that gets called by GPIO on a RPi channel rising edge. Counts
    gear teeth sensed by sensor 1 and 3. Sensor 2 is the quadrature sensor
    that determines whether sensor 1 and 3 teeth counted up or down.
    Assumes that sensor 3 is 180 degrees out of phase w.r.t sensor 1.

    Arguments:
    ch - the channels for sensor 1 or 3
    sdat - sensor data class 
    edgetype - should be "rising" or "falling"
    """

    if ((edgetype == 'falling') and (USEFALLINGEDGE == False))
        return

    # Sensor 1 just had an edge (since this callback function was called), so now
    # we need to find the state of sensor 2 to get the rotation direction.
    sensor2 = GPIO.input(gearsensor2_pin)
    now = time.time()
    newtcount1 = newtcount3 = deltat1 = deltat3 = 0

    if (ch == gearsensor1_pin or ch == gearsensor1b_pin):
        # increment/decrement tooth counter. If we're counting both riding
        # and falling edges, then each edge increments the tooth count by a half tooth.
        # pin1 is set up for rising edges, pin1b for falling edges
        if (USEFALLINGEDGE)
            stepsize = 0.5
        else
            stepsize = 1

        # We'll define the "forward" rotation direction as the one where
        # sensor 2 sees a tooth gap when sensor 1 senses a tooth rising edge
        if (((edgetype == 'rising') and (sensor2 == 0))
         or ((edgetype == 'falling') and (sensor2 == 1)))
            forwarddirection = True
        else
            forwarddirection = False

        # Change the tooth count depending on rotation direction, and on
        # which direction we want to count (set by COUNTDIR)
        step = COUNTDIR*stepsize if forwarddirection else -COUNTDIR*stepsize
        newtcount1 = sdat.getdata('tcount1') + step
        sdat.setdata('tcount1', newtcount1)
        print("ch1 -> edge:%s  step:%.1f  count:%.1f" % (edgetype, step, newcount1))

        # time since last sensor 1 tooth edge
        deltat1 = now - sdat.getdata('edge1time')
        speed = 1/deltat1 * 360/NTEETH   # speed is in teeth per second
        newangle = (newtcount1 % NTEETH)* 360/NTEETH

        sdat.setdata('angle', newangle)
        sdat.setdata('speed', speed)
        sdat.setdata('edge1time', now)
    else:
        # we're not processing sensor 3 edge data any more
        return

    angleM = sdat.getdata('angle')
    speedM = sdat.getdata('speed')
    print("ch1: %d | ch3: %d | %.1f deg | %.4f speed"
               % (sdat.getdata('tcount1'), sdat.getdata('tcount3'),
                  angleM, speedM) )
    message = "%s,%s" % (angleM, speedM)
    pub.raw_send(message, 'motion')

if __name__ == "__main__": 
    pub = util.PubClient('192.168.2.5', 'motion')
    gtsdata = gts_data()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gearsensor1b_pin, GPIO.IN)
    GPIO.setup(gearsensor2b_pin, GPIO.IN)
    GPIO.setup(gearsensor3b_pin, GPIO.IN)
    GPIO.setup(gearsensor1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(gearsensor2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(gearsensor3_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(gearsensor1_pin, GPIO.RISING,
                          callback=lambda ch: sensor_up(ch, gtsdata, "rising"))
    GPIO.add_event_detect(gearsensor1b_pin, GPIO.FALLING,
                          callback=lambda ch: sensor_up(ch, gtsdata, "falling"))

# we're not processing sensor 3 edges any more
#    GPIO.add_event_detect(gearsensor3_pin, GPIO.RISING,
#                          callback=lambda ch: sensor_up(ch, gtsdata, "rising"))
#    GPIO.add_event_detect(gearsensor3b_pin, GPIO.FALLING,
#                          callback=lambda ch: sensor_up(ch, gtsdata, "falling"))

    print("waiting for gear teeth")
    while True:
        try:
            curtime = time.time()
        except KeyboardInterrupt:
            GPIO.cleanup()
        time.sleep(5)

    GPIO.cleanup()
