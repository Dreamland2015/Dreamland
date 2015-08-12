import RPi.GPIO as GPIO
import time
import multiprocessing as mp
# from multiprocessing import Process as mp_Process, Array as mp_Array
# from multiprocessing import Value as mp_Value, Lock as mp_Lock

 
gearsensor1_pin = 16
gearsensor2_pin = 18

 
class gts_data(object):
	""" Class for gear tooth sensor data shared between processes """
	def __init__(self, angle=0, speed=0, edges1=0, edges2=0):
		self.lock = mp.Lock()
		self.angle = mp.Value('d', angle)
		self.speed = mp.Value('d', speed)
		self.edges1 = mp.Value('d', edges1)
		self.edges2 = mp.Value('d', edges2)
		self.edge1time = mp.Value('d', time.time())
		self.edge2time = mp.Value('d', time.time())
  
	def getdata(self, whichdata):
		with self.lock:
			if whichdata == 'angle':
				return self.angle.value
			elif whichdata == 'speed':
				return self.speed.value
			elif whichdata == 'edges1':
				return self.edges1.value
			elif whichdata == 'edges2':
				return self.edges2.value
			elif whichdata == 'edge1time':
				return self.edge1time.value
			elif whichdata == 'edge2time':
				return self.edge2time.value
			else:
				pass
 
	def setdata(self, whichdata, dat):
		with self.lock:
			if whichdata == 'angle':
				self.angle.value = dat
			elif whichdata == 'speed':
				self.speed.value = dat
			elif whichdata == 'edges1':
				self.edges1.value = dat
			elif whichdata == 'edges2':
				self.edges2.value = dat
			elif whichdata == 'edge1time':
				self.edge1time.value = dat
			elif whichdata == 'edge2time':
				self.edge2time.value = dat
			else:
				pass
 
def sensor_up(ch, sdat):
	""" Callback function for a rising edge on a sensor.  """
	now = time.time()
	
	if (ch == gearsensor1_pin):
		s2 = GPIO.input(gearsensor2_pin)
		forward = (s2==0)
		edgevar = 'edges1'
		deltat = now - sdat.getdata('edge1time')
		sdat.setdata('edge1time', now)
	elif (ch == gearsensor2_pin):
		s2 = GPIO.input(gearsensor1_pin)
		forward = (s2==1)
		edgevar = 'edges2'
		deltat = now - sdat.getdata('edge2time')
		sdat.setdata('edge2time', now)

	if forward==True:
		newedges = gtsdata.getdata(edgevar) + 1
	else:
		newedges = gtsdata.getdata(edgevar) - 1
		
	sdat.setdata(edgevar, newedges)
	print("sensed rising edge on channel %s - count = %d - delta t = %f"
               % (ch, newedges, deltat) )


if __name__ == "__main__":
	gtsdata = gts_data()

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(gearsensor1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(gearsensor2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	GPIO.add_event_detect(gearsensor1_pin, GPIO.RISING,
	                      callback=lambda ch: sensor_up(ch, gtsdata))
 
	print("waiting for gear teeth")
	while True:
		try:
				curtime = time.time()
		except KeyboardInterrupt:
				GPIO.cleanup()
		time.sleep(5)
 
	GPIO.cleanup()
