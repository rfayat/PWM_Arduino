# PWM_Arduino
Launch PWM on an arduino via a serial port using python

## Requirements -- Arduino
Install the [Arduino PWM Frequency Library](https://code.google.com/archive/p/arduino-pwm-frequency-library/downloads) from your arduino IDE.

## Setting up the hardware

**Warning:**
All pins do not support interruptions (e.g. [only pins 2 and 3 on the arduino Uno](https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/)), set `PIN_COUNTER` to a pin that can support interruptions.
