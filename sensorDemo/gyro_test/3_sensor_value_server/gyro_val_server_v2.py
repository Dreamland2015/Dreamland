#!/usr/bin/python
#
# Copied and modified from:
# http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html
#
# Runs on RPi
# Gets values from MPU-6050 sensor and presents them via a web server
#
 
# import smbus
import math
import time
import zmq
import random
import signal
from multiprocessing import Process as mp_Process, Array as mp_Array
from multiprocessing import Value as mp_Value, Lock as mp_Lock


# Configure ports
ip_addr = "127.0.0.1"
pub_port = "5600"
 
i2caddress = 0x68  # This is the address value read via the i2cdetect command
# Power management register (only first one is needed)
power_mgmt_1 = 0x6b
# The first address of the data block containing the gyro, temperature,
# and accelerometer values:
data_register = 0x3b
# data block length
data_length = 14

# scaling factors
gyro_scale = 131.0
accel_scale = 16384.0
temp_scale = 1 # 340.0	# temperature
gyro_x_offset = 0.0
gyro_y_offset = 0.0
gyro_z_offset = 0.0
temp_offset = 0 # -521.0  # temperature


# Enable interrupt with ctrl-C if that's not already set up
signal.signal(signal.SIGINT, signal.SIG_DFL)


class Gyrodata(object):
    """ Gyro data shared between processes """
    def __init__(self, initraw=None, initspeed=None, initangle=None):
        self.lock = mp_Lock()
#        initraw=[1,2,3,4,5,6,7] if initraw==None
        if initraw == None: initraw==[1, 2, 3, 4, 5, 6, 7]
        if initspeed == None: initspeed==123
        if initangle == None: initangle==499
        print("Gyrodata says: initializing data", flush=True)
        # raw values: rgyro_x, rgyro_y, rgyro_z, 
        #             raccel_x, raccel_y, raccel_z, rT
        self.rawdata = mp_Array('i', initraw)
        self.speed = mp_Value('d', initspeed)
        self.angle = mp_Value('d', initangle)
        print("Gyrodata says: angle value is: ", self.angle.value, flush=True)
        print("Gyrodata says: init changed angle value to: ", self.angle.value, flush=True)
        
    def getdata(self, whichdata):
        with self.lock:
            if whichdata == 'angle':
                return self.angle.value
            elif whichdata == 'speed':
                return self.angle.value
            elif whichdata == 'rawdata':
                return self.rawdata.value
            else:
                pass

    def setdata(self, whichdata, dat):
        with self.lock:
            if whichdata == 'angle':
                self.angle.value = dat
            elif whichdata == 'speed':
                self.speed.value = dat
            elif whichdata == 'rawdata':
                self.rawdata.value = dat
            else:
                pass

 
def read_sensor():
    global rgyro_x, rgyro_y, rgyro_z, raccel_x, raccel_y, raccel_z, rT
    # read all relevant data at once
    raw_data = bus.read_i2c_block_data(i2caddress, data_register, data_length)
    # parse data
    raccel_x = get_datavalue(raw_data, 0) / accel_scale
    raccel_y = get_datavalue(raw_data, 2) / accel_scale
    raccel_z = get_datavalue(raw_data, 4) / accel_scale
    rT = (get_datavalue(raw_data, 6) - temp_offset) / temp_scale
    rgyro_x = (get_datavalue(raw_data, 8) - gyro_x_offset) / gyro_scale
    rgyro_y = (get_datavalue(raw_data, 10) - gyro_y_offset) / gyro_scale
    rgyro_z = (get_datavalue(raw_data, 12) - gyro_z_offset) / gyro_scale
 
    return (rgyro_x, rgyro_y, rgyro_z, raccel_x, raccel_y, raccel_z, rT)


def get_datavalue(datablock, offset):
    """ return two's complement of two-byte data within data block"""
    high = datablock[offset]
    low = datablock[offset+1]
    val = (high << 8) + low
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val


def sensordata_process_loop(gyrodata):
    #bus = smbus.SMBus(1) # using bus 1 for Revision 2 boards
 
    # Now wake the 6050 up as it starts in sleep mode
    #bus.write_byte_data(i2caddress, power_mgmt_1, 0)
    print("started sensordata_process_loop", flush=True)
    startt = lasttime = lastprint = lastset = time.time()
    i = 0
    running = True
    current_angle = 0
    while running:
        now = time.time()
        deltat = now-lasttime
#        rgyro_x, rgyro_y, rgyro_z = read_sensor()[0:3]
        rgyro_z = 10 + random.random()  # for testing
        current_angle += deltat * rgyro_z
        i += 1
        if now-lastset > 0.5:
            lastset = now
            print("--- --- Sensordata process loop says: gyrodata was:", gyrodata.getdata('angle'), flush=True)
            gyrodata.setdata('angle', current_angle)
            print("--- --- Sensordata process loop says: resetting lastset: current_angle is now:", current_angle, flush=True)
            print("--- ---                                                  gyrodata is now:", gyrodata.getdata('angle'), flush=True)
        if now-lastprint > 2:
            lastprint=now
            print("--- --- Sensordata process loop says: resetting lastset: current_angle is now:", current_angle, flush=True)
            print("--- ---                                                  gyrodata is now:", gyrodata.getdata('angle'), flush=True)
            print("--- --- Sensordata process loop says: #{i:d}: Angle is {ang:f}".format(
                  i=i, ang=gyrodata.getdata('angle')), flush=True)
        lasttime=now
     
        if now-startt > 20:
            running = False
            print("--- --- Sensordata process loop done after 20 seconds", flush=True)


def sensordata_server(gyrodata):
    print("--- sensordata_server says: started", flush=True)
    
    context = zmq.Context()
    gserver = context.socket(zmq.REP)
    # setsockopt must come before bind or connect
    # set high water marks, so no more than 2 messages are queued up in mem
    gserver.setsockopt(zmq.SNDHWM, 2)
    gserver.setsockopt(zmq.RCVHWM, 2)
    # set linger so no queued up messages remain when process exits
    gserver.setsockopt(zmq.LINGER, 0)
    
    gserver.bind("tcp://" + ip_addr + ":" + pub_port)
    
    # set up polling of sockets. We're only adding/registering the gserver
    # to the sockets to be polled whether they have a request in them
    poller = zmq.Poller()
    poller.register(gserver, zmq.POLLIN)
    
    print("--- sensordata_server says: Sockets started", flush=True)
    running = True
    while running:
        # check whether there's a request on the socket (only one so far)
        sockets = dict(poller.poll())
        
#        if sock in socks and socks[socket]=zmq.POLLIN:
        if gserver in sockets:
            request = gserver.recv_string()
            print("--- sensordata_server says: someone requested ", request, flush=True)
            if request == "End":
                running = False
            else:
                reply_data = gyrodata.getdata(request)
                print("--- sensordata_server says: I'm sending back ", reply_data, flush=True)
                gserver.send_pyobj(reply_data)
    print("--- sensordata_server says: Ending", flush=True)


def test_client():
    context = zmq.Context()
    gserver = context.socket(zmq.REQ)
    # setsockopt must come before bind or connect
    # set high water marks, so no more than 2 messages are queued up in mem
    gserver.setsockopt(zmq.SNDHWM, 2)
    gserver.setsockopt(zmq.RCVHWM, 2)
    # set linger so no queued up messages remain when process exits
    gserver.setsockopt(zmq.LINGER, 0)
    gserver.connect("tcp://" + ip_addr + ":" + pub_port)
    
    print("  test_client says: Sockets started", flush=True)
    for i in range(0,10):
        print("  test_client says: sending angle request ", i, flush=True)
        gserver.send_string("angle")
        angle = gserver.recv_pyobj()
        print("  test_client sayd: got answer angle: ", angle, flush=True)
        time.sleep(3)
    print("  test_client sayd: Sending end request", flush=True)
    gserver.send_string("End")
    print("  test_client sayd: Ending", flush=True)
        

if __name__ == "__main__":
    initraw=[1, 22, 333, 412, -50, -66, 7000]
    gyro = Gyrodata(initraw, 111, 222)
     
    sensor_loop = mp_Process(name='sensordataloop1',
                             target=sensordata_process_loop, args=(gyro,))
    server = mp_Process(name='sensordataserver1',
                        target=sensordata_server, args=(gyro,))
    client = mp_Process(name='testclient1', target=test_client)

    sensor_loop.start()
    server.start()
    client.start()
    
    client.join()
    server.join()
    sensor_loop.join()
    
#    c = raw_input("Type something to quit.")  # python 2
#    print("done", flush=True)
 
#    print(read_all())
#    print("Determining offsets: Don't move sensor")
#    readings_sum = np.array([0,0,0,0,0,0,0])
#    startt = time.time()
#    for i in range(1000):
#        readings = np.array(read_sensor())
#        readings_sum = readings_sum + readings
#    readings_avg = readings_sum / 1000
#    (gyro_xoffset, gyro_yoffset, gyro_zoffset) = readings_avg[0:3] * gyro_scale
#     print(read_all())
#     print(readings_sum)
#    print(readings_avg)
#    print("time diff: %f" % (time.time() - startt))
#    print("done calibrating")
     
