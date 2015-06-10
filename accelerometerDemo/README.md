Dreamland
=========
## Accelerometer connection demos for Raspberry Pi

We're trying to set up an accelerometer / gyro to sense rotation in the
dreamland wheel.

About the accelerometer / gyro:

- We're using the MPU-6050, which is a chip with a 3-axis accelerometer, and a
  3-axis gyroscope. It should be sensitive enough to handle slow rotations.
  
- Several vendors sell the chip on a breakout board, which allows us to connect
  to it easily.

- Example vendors: (note the huge variation in price)
  Sparkfun: https://www.sparkfun.com/products/11028  ($40)
  Amazon: http://www.amazon.com/gp/product/B00H1OYE4Q/ref=oh_aui_detailpage_o00_s01?ie=UTF8&psc=1  ($12)
  Ebay: as low as $1, or $2 with free shipping from Hong Kong...

  
Things still to be worked out:

- If the sensor is mounted close to the roation axis, all accelerometers will
  read a constant value (zero for two of them, and Earth gravity for the
  downward one). Only one of the gyros will read rotation speed.
  If the sensor is mounted far out on a wheel arm, one horizontal accelerometer
  will sense centripetal acceleration, and the other rotation speedup.
  This could help with sensing zero rotation.
  
- The gyro does suffer from a zero offset, which supposedly even varies
  with temperature (i.e. all the time at Burning Man). So it's hard to verify
  that the wheel is not rotating, and not possible to get wheel position
  
- An alternative would be to set up a rotary encoder, or a gear tooth sensor.
  That would easily give rotation and position information.
  But where / how to set this up?
  
- A magnetic compass could help with position/orientation sensing. But our
  structure is mostly magnetic steel. Maybe it still works if we only need
  to get an index orientation...

  
  