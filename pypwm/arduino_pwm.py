"""Send parameters and start/stop signals to an arduino running PWM.

Author: Romain Fayat, October 2021
"""
import serial
import time
from functools import wraps


def check_success(f):
    "Add a check that the arduino sent feedback to a method."
    @wraps(f)
    def g(self, *args, **kwargs):
        "Run the wrapped method and return a boolean indicating success."
        f(self, *args, **kwargs)
        time.sleep(1.)
        is_success = self.readline_last() == "success"
        if is_success:
            print("Received 'success' via the serial port.\n")
        else:
            print("Did NOT receive 'success' via the serial port.\n")
        return is_success

    return g


def check_object_type(obj, type):
    "Check that obj is an instance of type and throws a ValueError if not."
    try:
        assert isinstance(obj, type)
    except AssertionError:
        raise ValueError("Input doesn't match expected type.")


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
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self.chunk_size = chunk_size
        self.chunk_pause = chunk_pause
        self.check_input_types()
        super().__init__(*args, **kwargs)
        time.sleep(3.)
        print(f"Connected to Arduino on port {self.name}\n")
        self.set_pwm_parameters()
        time.sleep(1.)

    def check_input_types(self):
        "Make sure the user-provided PWM parameters are valid."
        if not isinstance(self.frequency, int):
            raise ValueError("frequency must be an integer.")
        if not isinstance(self.duty_cycle, float) or self.duty_cycle < 0 or self.duty_cycle > 1:  # noqa 501
            raise ValueError("duty_cycle must be a float between 0. and 1.")
        if not isinstance(self.chunk_size, int):
            raise ValueError("chunk_size must be an integer.")
        if not isinstance(self.chunk_pause, int):
            raise ValueError("chunk_pause must be an integer.")

    @property
    def available(self):
        "Return a boolean indicating if any content is in the buffer."
        return self.in_waiting > 0

    def write(self, data):
        "Convert data to bytes and write it via the serial port."
        formatted = bytes(str(data), encoding="utf-8")
        super().write(formatted)
        print(f"Sent: {formatted}")

    def readline(self):
        "Read a line from the serial connection, return None if empty."
        if self.available:
            line = super().readline().decode("ascii")
            return line.rstrip("\n")
        else:
            return None

    def readline_last(self):
        "Return the value of the last line in the buffer."
        if self.available:
            while self.available:
                last_line = self.readline()
            return last_line
        else:
            return None

    @check_success
    def set_pwm_parameters(self):
        "Send the PWM parameters to the arduino."
        # Conversion of the duty cycle to a byte
        duty_cycle_converted = int(self.duty_cycle * 255)
        self.write(
            f"parameters\n{self.frequency}\n{duty_cycle_converted}\n{self.chunk_size}\n{self.chunk_pause}\n"  # noqa E501
        )

    @check_success
    def start_pwm(self):
        "Send the start order to the arduino."
        self.write("start\n")

    @check_success
    def stop_pwm(self):
        "Send the stop signal to the arduino."
        self.write("stop\n")

    def close(self):
        "Send a stop signal and close the serial connection."
        self.stop_pwm()
        time.sleep(2.)
        super().close()


if __name__ == "__main__":
    ser = Arduino_PWM("/dev/ttyACM0",
                      timeout=.1,
                      frequency=1,
                      chunk_size=10,
                      chunk_pause=5000)
    ser.start_pwm()
    try:
        while True:
            time.sleep(.1)

    except KeyboardInterrupt:
        print("Hit ctrl-C")
    finally:
        print("Cleaning up")
        ser.close()
