Dreamland
=========
## Accelerometer connection demos for Raspberry Pi

We're trying to set up an accelerometer / gyro to sense rotation in the dreamland wheel.

### Read gyro values and calculate angle

gyrotest3.py  
This code runs on the RPi.

The code reads angular speed data from the MPU-6050 gyros and tries to integrate the values to get angle. The code prints the numbers to stdout every 2 seconds.