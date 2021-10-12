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
        # self.test_connection()
        self.set_pwm_parameters(frequency=frequency, duty_cycle=duty_cycle,
                                chunk_size=0, chunk_pause=1000)

    def write(self, data):
        "Convert data to bytes and write it via the serial port."
        formatted = format_data(data)
        super().write(formatted)
        print(f"Sent: {formatted}")

    def write_readline(self, data):
        "Write data on the serial port and return a response."
        self.write(data)
        time.sleep(1e-1)
        answer = self.readline()
        print(f"Received: {answer}")
        return answer

    def test_connection(self):
        "Test the connection to the arduino and return a boolean."
        try:
            self.read()
            print(f"Connected to Arduino on port {self.name}")
            return True
        except serial.serialutil.SerialException as err:
            print(f"Connection to arduino failed:\n{err}")
            return False

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
    ser = Arduino_PWM("/dev/ttyACM0", timeout=.1)
    try:
        ser.test_connection()
        s = str(input("Send something to the Arduino: "))
        ser.write_readline(s)
        while True:
            time.sleep(1e-6)
    except KeyboardInterrupt:
        print("Hit ctrl-C")
    finally:
        print("Cleaning up")
        ser.close()
