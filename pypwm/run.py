"""Run PWM on an arduino using Python.

Author: Romain FAYAT, November 2021
"""
import argparse
from pathlib import Path
import json
import sys
import time
from .arduino_pwm import Arduino_PWM

# Argument parsing
parser = argparse.ArgumentParser(__doc__)
parser.add_argument("-P", "--port", default="ttyACM0",
                    help="Serial port the arduino is attached to, default: ttyACM0.")  # noqa E501
parser.add_argument("-f", "--frequency", default=30, type=int,
                    help="PWM frequency in Herz, int, default: 30.")
parser.add_argument("-c", "--chunk_size", default=0, type=int,
                    help="Number of frames per chunk, int, default: 0 (continuous PWM).")  # noqa E501
parser.add_argument("-d", "--duty_cycle", default=.5, type=float,
                    help="Duty cycle, float between 0 and 1, default: .5.")
parser.add_argument("-p", "--chunk_pause", default=1000, type=int,
                    help=("Pause between chunks in ms, int, default: 1000."
                          " Ignored if chunk_size is 0 (continuous PWM)."))
parser.add_argument("--test_connection", const=True,
                    default=False, action="store_const",
                    help="Connect to the Arduino without running PWM.")
parser.add_argument("--json", default=None, dest="path_parameters",
                    help=("Path to an input parameter file. "
                          "Values in the json override other inputs."),
                    type=lambda x: Path(x).expanduser())

# Argument parsing
args = parser.parse_args()
port = args.port
frequency = args.frequency
chunk_size = args.chunk_size
duty_cycle = args.duty_cycle
chunk_pause = args.chunk_pause

# Read the json and override the parameter values if provided in the json
if args.path_parameters is not None:
    with args.path_parameters.open("r") as json_file:
        json_params = json.load(json_file)
    # Deals with imbricated json parameters
    if "pwm" in json_params:
        json_params = json_params["pwm"]
    # Parse input parameters, keeping provided values as default
    port = json_params.get("port", port)
    frequency = int(json_params.get("frequency", frequency))
    duty_cycle = float(json_params.get("duty_cycle", duty_cycle))
    chunk_size = int(json_params.get("chunk_size", chunk_size))
    chunk_pause = int(json_params.get("chunk_pause", chunk_pause))

# Add /dev at the beginning of the provided port if needed
if not port.startswith("/dev"):
    port = "/dev/" + args.port

if __name__ == "__main__":
    ser = Arduino_PWM(port, timeout=.1, frequency=frequency,
                      chunk_size=chunk_size, chunk_pause=chunk_pause,
                      duty_cycle=duty_cycle)

    # If test_connection is set to True, simply close the connexion and exit
    if args.test_connection:
        ser.close()
        sys.exit()
    ser.start_pwm()
    try:
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        print("Hit ctrl-C")
    finally:
        print("Cleaning up")
        ser.close()
