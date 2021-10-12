#ifndef serial_helpers
#define serial_helpers
int32_t FREQUENCY;  // Hz
byte DUTY_CYCLE; // 0-255, 128 corresponds to a 50% duty cycle
int CHUNK_SIZE;  // Number of PWM cycles before starting a pause
int INTERRUPTION_TIME; // duration of the pauses, ms

bool read_parameters(){
  FREQUENCY = 10;
  DUTY_CYCLE = 128;
  CHUNK_SIZE = 50;
  INTERRUPTION_TIME = 1000;
  return true;
}

#endif
