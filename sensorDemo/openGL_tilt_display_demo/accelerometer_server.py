#!/usr/bin/python

# This program reads accelerometer + Gyro data from an accelerometer board
# with MPU-6050 chip, using the i2c protocol. It then presents the data
# via a webserver.
# This program should be run on a Raspberry Pi (version B+ or 2 B) that
# is connected to that chip.
#
# Copied and modified from:
# http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html

import web
import smbus
import math


# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

urls = (
    '/', 'index'
)

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


class index:
    def GET(self):
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)

        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0

        x_rot = get_x_rotation(accel_xout_scaled, accel_yout_scaled,
                               accel_zout_scaled)
        y_rot = get_y_rotation(accel_xout_scaled, accel_yout_scaled,
                               accel_zout_scaled)

        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)

        gyro_xout_scaled = gyro_xout / 131
        gyro_yout_scaled = gyro_yout / 131
        gyro_zout_scaled = gyro_zout / 131


        return str(x_rot) + " " + str(y_rot) + " " + \
               str(gyro_zout_scaled)


if __name__ == "__main__":

    # Now wake the 6050 up as it starts in sleep mode
    bus.write_byte_data(address, power_mgmt_1, 0)

    app = web.application(urls, globals())
    app.run()
