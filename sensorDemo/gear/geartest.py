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
			else:
				pass
 
def sensor_edge(ch, edge, sdat):
	""" 
	Callback function for an edge on a sensor.
	Count edges (gear teeth) forward or backward for either sensor.
	"""
	curtime = time.time()
	
	if (ch = gearsensor1_pin):
		edgevar = 'edges1'
		s2 = GPIO.input(gearsensor2_pin)
	elif (ch = gearsensor2_pin):
		edgevar = 'edges2'
		s2 = GPIO.input(gearsensor1_pin)

	forward = ((edge=='rising') is not (s2==1))
	if forward==1:
		newedges = gtsdata.getdata(edgevar) + 1
	else:
		newedges = gtsdata.getdata(edgevar) - 1
		
	sdat.setdata(edgevar, newedges)
	
	
	print("sensed rising edge on channel - count = %d" % newedgest1 )


def sensor1_edge(ch, edge, sdat):
	""" Callback function for an edge on a sensor1, counting gear tooth edges. """
	curtime = time.time()
	
	s2 = GPIO.input(gearsensor2_pin)	# check sensor 2 level
	forward = ((edge=='rising') is not (s2==1))

	if forward==True:
		newedgecount = gtsdata.getdata('edges1') + 1
	else:
		newedgecount = gtsdata.getdata('edges1') - 1
		
	sdat.setdata('edges1', newedgecount)
	
	print("sensed rising edge on channel - count = %d" % newedgest1 )

	 
#def sensor1_down(channel):
#	   s2 = GPIO.input(gearsensor2_pin)
#	   if s2==1:
#			   edgecount1 += 1
#	   else:
#			   edgecount1 -= 1
#	   print("detector1 sensed falling edge - count = %d" % edgecount1 )


if __name__ == "__main__":
	gtsdata = gts_data()

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(gearsensor1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(gearsensor2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	GPIO.add_event_detect(gearsensor1_pin, GPIO.RISING,
	                      callback=lambda ch: sensor1_up(ch, 'rising', gtsdata))
	GPIO.add_event_detect(gearsensor1_pin, GPIO.FALLING, 
	                      callback=lambda ch: sensor1_up(ch, 'falling', gtsdata))
 
	while True:
		try:
				curtime = time.time()
				print("waiting for gear tooth")
		except KeyboardInterrupt:
				GPIO.cleanup()
		time.sleep(3)
 
	GPIO.cleanup()
