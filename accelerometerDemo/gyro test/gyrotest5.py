#!/usr/bin/python
#
# Copied and modified from:
# http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html
 
import smbus
import math
import time
import numpy as np
import thread
import zmq
from multiprocessing import Process
 
# Configure ports
send_port = "5560"
recv_port = "5559"
 
i2caddress = 0x68  # This is the address value read via the i2cdetect command
# Power management register (only first one is needed)
power_mgmt_1 = 0x6b
# The first address of the data block containing the gyro, temperature,
# and accelerometer values:
data_register = 0x3b
data_length = 14    # data block length
 
gyro_scale = 131.0
accel_scale = 16384.0
temp_scale = 1 # 340.0	# temperature
gyro_x_offset = 0.0
gyro_y_offset = 0.0
gyro_z_offset = 0.0
temp_offset = 0 # -521.0  # temperature
# raw data values
(rgyro_x, rgyro_y, rgyro_z, raccel_x, raccel_y, raccel_z, rT) = 5,0,0,0,0,0,0

 
def read_sensor():
    global rgyro_x, rgyro_y, rgyro_z, raccel_x, raccel_y, raccel_z, rT
    # read all relevant data at once
    raw_data = bus.read_i2c_block_data(i2caddress, data_register, data_length)
    # parse data
    raccel_x = get_value(raw_data, 0) / accel_scale
    raccel_y = get_value(raw_data, 2) / accel_scale
    raccel_z = get_value(raw_data, 4) / accel_scale
    rT = (get_value(raw_data, 6) - temp_offset) / temp_scale
    rgyro_x = (get_value(raw_data, 8) - gyro_x_offset) / gyro_scale
    rgyro_y = (get_value(raw_data, 10) - gyro_y_offset) / gyro_scale
    rgyro_z = (get_value(raw_data, 12) - gyro_z_offset) / gyro_scale
 
    return (rgyro_x, rgyro_y, rgyro_z, raccel_x, raccel_y, raccel_z, rT)

def get_value(datablock, offset):
    """ return two's complement of two-byte data within data block"""
    high = datablock[offset]
    low = datablock[offset+1]
    val = (high << 8) + low
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

class index:
    def GET(self):
        global rgyro_x, rgyro_y, rgyro_z, raccel_x, raccel_y, raccel_z, rT
        rgyro_x += 1
        print("checking get global access:")
        printglobal()
        print("inside get: %s" % rgyro_x)
        output = str(rgyro_x)+" "+str(rgyro_y)+" "+str(rgyro_z)+" "
        output += str(raccel_x)+" "+str(raccel_y)+" "+str(raccel_z)+" "
        output += str(rT)
        return output
        
def printglobal():
    global rgyro_x, rgyro_y, rgyro_z, raccel_x, raccel_y, raccel_z, rT
    print("inside printglobal: %s" % rgyro_x)
    
        
def change_rx():
    global rgyro_x, rgyro_y, rgyro_z, raccel_x, raccel_y, raccel_z, rT
    rgyro_x = 789
 
if __name__ == "__main__":
    bus = smbus.SMBus(1) # using bus 1 for Revision 2 boards
 
    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(i2caddress, power_mgmt_1, 0)
     
    app = web.application(urls, globals())
    thread.start_new_thread( app.run, () )
    
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
     
    angle = 0
     
    running=1
    startt = lasttime = lastprint = time.time()
    print("inside main: %d" % rgyro_x)
    while running:
        now = time.time()
        deltat = now-lasttime
#        rgyro_x, rgyro_y, rgyro_z = read_sensor()[0:3]
        angle += deltat * rgyro_z
        
        if now-lastprint > 2:
            lastprint=now
#            print("Angle is %.3f - gx,gy,gz= %.3f %.3f %.3f" % (angle, gyro_x, gyro_y, gyro_z))
            print(rgyro_x)
            rgyro_x, rgyro_y, rgyro_z = read_sensor()[0:3]
            print(rgyro_x)
            change_rx()
            print(rgyro_x)
            print("angle,gx,gy,gz= %.3f %.3f %.3f %.3f" % (angle, rgyro_x, rgyro_y, rgyro_z))
            printglobal()
        lasttime=now
     
        if now-startt > 20:
            running = False
            print("done after 20 seconds")
