# PWM_Arduino
Launch PWM on an arduino via a serial port using python


## Python handling of the serial connexion
Clone the repository and install the package as follows:
```bash
$ https://github.com/rfayat/PWM_Arduino.git
$ cd PWM_Arduino
$ pip install .
```

You can then run PWM by simply running:
```bash
$ python -m pypwm.run
```

Parameters can also be set directly in the command line or using a json file. For this parameter file, valid keys are `port`, `frequency`, `chunk_size`, `chunk_pause` and `duty_cycle`. Missing parameters will be set to their default value or the one provided in the command line if any was provided. You can refer to the the script's documentation for default values and valid inputs by running:
```bash
$ python -m pypwm.run --help
```

## Arduino setup
### Dependencies and code upload
Install the [Arduino PWM Frequency Library](https://code.google.com/archive/p/arduino-pwm-frequency-library/downloads) from your arduino IDE. This library is compatible with arduino Uno.
To install it, download the zip file, extract it and place the directory `PWM` inside /path/to/Arduino/libraries/

You can then upload the code in the repository's [pwm_arduino](pwm_arduino) folder to your arduino.

### Setting up the hardware
Circuit, for an arduino Uno:
TODO: Add illustration

**Warning:**
All pins do not support interruptions (e.g. [only pins 2 and 3 on the arduino Uno](https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/)), set `PIN_COUNTER` to a pin that can support interruptions.
