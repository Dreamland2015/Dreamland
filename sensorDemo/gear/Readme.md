Dreamland
=========
## Wiring for the gear tooth sensor 

Here's an image of the gear tooth sensor setup:  

local image copy:  
![Gearsensor setup](gearsensor_plate.png?raw=true)

![Gearsensor setup](https://github.com/Dreamland2015/Dreamland/blob/master/sensorDemo/gear/gearsensor_plate.png?raw=true)

This is a view from above.
Sensor 1 is the rightmost one, the one that sees a tooth first if the gear flange is rotating clockwise.

There are 5 wires connecting the sensors: Power (5V), Ground, Sensor out 1, Sensor out 2, Sensor out 3. Sensor 1 and 2 are the main sensors, and set up 90 degrees out of phase on the gear tooth flange (1/2 tooth apart) so the combination acts as quad sensor.
Sensor 3 is a spare that can substitute for Sensor 1.

Each sensor sensor has 4 pins, which are connected like this:

Sensor chip:\
Pin 4 (GND), Pin 3 -->  RPi GPIO Ground pin\
Pin 2 (sensor output)--> RPi GPIO in pin\
Pin 1 (power) --> RPi +5V pin

Each sensor output pin gets connected to a GPIO pin that is configured with pullup resistor. Actually we're connecting it to a second pin in addition, which is configured as general input without pullup. The sensor output is a open collector, so it either floats (the RPi internal pullup resistor pull the voltage up, and the pin will sense 3.3V) or pulls to ground (the RPi pin will sense 0V)
Since the GPIO package only allows sensing either rising or falling edges, not both, by connecting to two pins we can detect both.

Wire colors for sensor setup 1 (to follow wires in case there is a cable problem):

| Setup 1                   |     Sensor 1     |          Sensor 2          |       Sensor 3      |  Power |     Ground     |
|---------------------------|:----------------:|:--------------------------:|:-------------------:|:------:|:--------------:|
| Sensor_pin                |         2        |              2             |          2          |    1   |        4       |
| Sensor_wire_color         |      yellow      |            white           |         blue        |   red  |      black     |
| white_ethernet_cable_wire |       green      |            brown           |         blue        | orange | 4x_white_wires |
| [RJ-45 socket connector]  |                  |                            |                     |        |                |
| gray cat5 cable           |       green      |            brown           |         blue        | orange | 4x_white_wires |
| header pin single wire    |         -        |              -             |          -          |   red  |        -       |
| header connector cable    |    red + pink    | white + green/yellowstripe |    brown + black    |    -   |      green     |
| Rpi GPIO pin              | 15(pink)+16(red) |     18(white)+19(g/ys)     | 21(brown)+22(black) | 2 or 4 |                |

The header connector at the end of the Cat5 cable should be connected with the "USB" writing towards the edge of the RPi, and positioned so the pink and red wires are on pin 15 and 16.
