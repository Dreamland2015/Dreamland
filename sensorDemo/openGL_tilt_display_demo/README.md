Dreamland
=========
## Accelerometer connection demo for Raspberry Pi

Demo code to read accelerometer data with a Raspberry Pi (version B+ or 2B) from a connected MPU-6050 accelerometer/gyro breakout board

### Files:
- accelerometer_server.py

     runs on the RPi, reads the data from the MPU-6050, using the i2c protocol, and presents the values on a web server. run with:
     
     python accelerometer_server.py
     
     and exit with ctrl-C when done with the demo.
     
     This needs to run with python 2, because is uses webpy, and there's currently no version of webpy for python3. That's fine for the demo though. It does require that i2c is enabled, and smbus is installed for for python 2.

- leveldemo.py

  just nicely displays the data presented on the web. It runs on a PC, reads the data from the RPi web server, and draws an OpenGL box tilting around, and in general mirroring what the accelerometer does.
  
  This runs in python3, probably also in python2.

Files taken and modified from the tutorial at:

http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html
