#!/usr/bin/python
#
# Copied and modified from:
# http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html
#
# First test of reading gyro & accelerometer values from the MPU-6050
# Runs on Raspberry Pi, outputs values to stdout.
#
# I think this works.

import smbus
import math
import time
import numpy as np

# Power management registers
power_mgmt_1 = 0x6b
# power_mgmt_2 = 0x6c   # not used

gyro_scale = 131.0
accel_scale = 16384.0
temp_scale = 1 # 340.0

gyro_xoffset = 0.0
gyro_yoffset = 0.0
gyro_zoffset = 0.0
temp_offset = 0 # -521.0

i2caddress = 0x68  # This is the address value read via the i2cdetect command

def read_all():
#    raw_gyro_data = bus.read_i2c_block_data(i2caddress, 0x43, 6)
#    raw_accel_data = bus.read_i2c_block_data(i2caddress, 0x3b, 6)
    raw_data = bus.read_i2c_block_data(i2caddress, 0x3b, 14)

    accel_x = read_word(raw_data[0], raw_data[1] ) / accel_scale
    accel_y = read_word(raw_data[2], raw_data[3] ) / accel_scale
    accel_z = read_word(raw_data[4], raw_data[5] ) / accel_scale
    temperature = (read_word(raw_data[6], raw_data[7]) - temp_offset) / temp_scale
    gyro_x  = (read_word(raw_data[8],  raw_data[9])  - gyro_xoffset) / gyro_scale
    gyro_y  = (read_word(raw_data[10], raw_data[11]) - gyro_yoffset) / gyro_scale
    gyro_z  = (read_word(raw_data[12], raw_data[13]) - gyro_zoffset) / gyro_scale

    return (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, temperature)

def read_word(byteHi,byteLo):
    return twos_complement((byteHi << 8) + byteLo)

def twos_complement(val):
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a * a) + (b * b))


bus = smbus.SMBus(1) # using bus 1 for Revision 2 boards

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(i2caddress, power_mgmt_1, 0)


print(read_all())
print("Determining offsets: Don't move sensor")
readings_sum = np.array([0,0,0,0,0,0,0])
startt = time.time()
for i in range(1000):
    readings = np.array(read_all())
    readings_sum = readings_sum + readings
readings_avg = readings_sum / 1000


(gyro_xoffset, gyro_yoffset, gyro_zoffset) = readings_avg[0:3] * gyro_scale
# print(read_all())
# print(readings_sum)
print(readings_avg)
print("time diff: %f" % (time.time() - startt))
print("done calibrating")

angle = 0

running=1
startt = lasttime = lastprint = time.time()
while running:
    now = time.time()
    deltat = now-lasttime
    (gyro_x, gyro_y, gyro_z) = read_all()[0:3]
    angle += deltat * gyro_z

    if now-lastprint > 2:
        lastprint=now
        print("Angle is %.3f - gx,gy,gz= %.3f %.3f %.3f" % (angle, gyro_x, gyro_y, gyro_z))
    lasttime=now

#     if now-startt > 20:
#          running = False
