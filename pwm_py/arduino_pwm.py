"""Send parameters and start/stop signals to an arduino running PWM.

Author: Romain Fayat, October 2021
"""
import serial
import time


def format_data(data):
    "Convert data to bytes after adding < and > around it."
    return bytes(str(data), encoding="utf-8")


class Arduino_PWM(serial.Serial):
    "Class for controlling an arduino running PWM."

    def __init__(self, *args, frequency=100, duty_cycle=.5, chunk_size=0,
                 chunk_pause=1000, **kwargs):
        """Create the serial object and set the pwm parameters.

        Parameters
        ----------
        *args, **kwargs
             Parameters for the serial connection, see serial.Serial

        frequency, int (default: 100)
            Frequency for the PWM, in Herz.

        duty_cycle, float (default: .5)
            Duty cycle for the PWM, between 0. and 1.

        chunk_size, int (default: 0)
            Number of PWM cycle before making a break in PWM.
            If 0 is provided, the arduino will generate continuous PWM.

        chunk_pause, int (default: 1000)
            Pause between PWM chunks if chunk_size != 0, in ms.

        """
        super().__init__(*args, **kwargs)
        time.sleep(5.)
        print(f"Connected to Arduino on port {self.name}")
        self.set_pwm_parameters(frequency=frequency, duty_cycle=duty_cycle,
                                chunk_size=0, chunk_pause=1000)

    @property
    def available(self):
        "Return a boolean indicating if any content is in the buffer."
        return self.in_waiting > 0

    def write(self, data):
        "Convert data to bytes and write it via the serial port."
        formatted = format_data(data)
        super().write(formatted)
        print(f"Sent: {formatted}")

    def readline(self):
        "Read a line from the serial connection, return None if empty."
        if self.available:
            line = super().readline()
            line = str(line)
            return line.rstrip("\n")
        else:
            return None

    def set_pwm_parameters(self, frequency, duty_cycle,
                           chunk_size, chunk_pause):
        "Send the PWM parameters to the arduino."
        # Conversion of the duty cycle to a byte
        duty_cycle_converted = int(duty_cycle * 255)
        pass

    def start_pwm():
        "Send the start order to the arduino."
        pass

    def stop_pwm():
        "Send the stop signal to the arduino."
        pass


if __name__ == "__main__":
    ser = Arduino_PWM("/dev/ttyACM1", timeout=.1)
    try:
        ser.write("parameters\n10\n128\n40\n5000\n")
        time.sleep(.1)
        while True:
            line = ser.readline()
            if line is not None:
                print(f"Received {line}")
            time.sleep(1.)

    except KeyboardInterrupt:
        print("Hit ctrl-C")
    finally:
        print("Cleaning up")
        ser.close()
