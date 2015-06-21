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

# Enable interrupt with ctrl-C if that's not already set up
signal.signal(signal.SIGINT, signal.SIG_DFL)
 
# Configure ports
send_port = "5560"
recv_port = "5559"
 
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


class Gyrodata(object):
    """ Gyro data shared between processes """
    def __init__(self, initdata=[1, 2, 33, 444, -5, -66, 70000]):
        # raw values: rgyro_x, rgyro_y, rgyro_z, raccel_x, raccel_y, raccel_z, rT
        self.rawdata = mp_Array('i', initdata)
        # processed values: speed, angle
        self.speed = mp_Value('d', 123)
        self.angle = mp_Value('d', 456)
        print("init: self.angle.value is: ", self.angle.value)
        self.lock = mp_Lock()

    def set_rawdata(self, arr):
        with self.lock:
            self.rawdata.value = arr
            
    def rawdata(self):
        with self.lock:
            return self.rawdata.value

    def set_speed(self, speed):
        with self.lock:
            self.speed.value = speed
            
    def speed(self):
        with self.lock:
            return self.speed.value

    def set_angle(self, angle):
        with self.lock:
            self.angle.value = angle

    def angle(self):
        with self.lock:
            return self.angle.value

 
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


def sensordata_process_loop():
    #bus = smbus.SMBus(1) # using bus 1 for Revision 2 boards
 
    # Now wake the 6050 up as it starts in sleep mode
    #bus.write_byte_data(i2caddress, power_mgmt_1, 0)
    print("started sensor server")
    gyro = Gyrodata()
    startt = lasttime = lastprint = time.time()
    i = 0
    running = True
    while running:
        now = time.time()
        deltat = now-lasttime
#        rgyro_x, rgyro_y, rgyro_z = read_sensor()[0:3]
        rgyro_z = 10 + random.random()  # for testing
        gyro.angle.value += deltat * rgyro_z
        i += 1
        if now-lastprint > 2:
            lastprint=now
            print("Sensorserver {i:d}: Angle is {ang:f}".format(
                  i=i, ang=gyro.angle.value))
        lasttime=now
     
        if now-startt > 20:
            running = False
            print("done after 20 seconds")

def sensordata_server():
    pass

def test_client():
    pass

if __name__ == "__main__":
     
    sensor_loop = mp_Process(name='sensordataloop1', 
                             target=sensordata_process_loop)
    server = mp_Process(name='sensordataserver1', target=sensordata_server)
    client = mp_Process(name='testclient1', target=test_client)

    sensor_loop.start()
    server.start()
    client.start()
    
    client.join()
    server.join()
    sensor_loop.join()
    
#    c = raw_input("Type something to quit.")  # python 2
#    print("done")
 
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
     
