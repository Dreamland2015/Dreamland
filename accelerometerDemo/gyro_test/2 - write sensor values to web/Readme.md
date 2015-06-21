Dreamland
=========
## Accelerometer connection demos for Raspberry Pi

We're trying to set up an accelerometer / gyro to sense rotation in the dreamland wheel.

### Write sensor values to web

gyrotest5.py  
This code runs on the Raspberry Pi.

This is an early example that runs, but doesn't work as intended. But parts of that code are useful for reuse.

I wanted to calculate the angle from the rotation speed I'm reading from the MPU-6050 gyros; basically integrating over time. I then wanted to periodically make these values available on the web server.

The raspberry pi needs to read the accelerometer/gyro often and quickly, so that it can sense speed changes and calculate a proper absolute angle. Meaning it can't wait around for some web client to connect asking for the values...

So we need to put that in a separate process thread. The problem is that the web server is also running in its own thread. How is it supposed to get the current data from the accelerometer thread?

I (foolishly) thought that the web server could just read a global variable that the accelerometer thread writes. That doesn't work, because each new thread gets its own personal set of global variables, so they aren't shared. So the web server happily writes its own global values to the web, which don't change.

How to solve this next time? Use zmq to do messaging between processes, and between Raspberry Pis or PCs.

The program uses code taken from:  
http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html