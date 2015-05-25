Dreamland
=========
## Accelerometer connection demo for Raspberry Pi

Files for reading accelerometer data with a Raspberry Pi (version B+ or 2B)
from a connected MPU-6050 accelerometer/gyro breakout board

accelerometer_server.py runs on the RP, reads the data from the MPU-6050, and
presents the values on a web server.
leveldemo.py runs on a PC, reads the data from the web server, and draws
an OpenGL box mirroring what the accelerometer does.

Files taken and modified from the tutorial at:
http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html
