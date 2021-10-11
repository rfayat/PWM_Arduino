/*
  Use a serial port input to parametrize and run PWM on an arduino.
*/
// Define the parameters
#include <PWM.h>
#define PIN_PWM 9
#define PIN_RUNNING 8
#define PIN_ENABLE 10
bool running = false;
byte duty_cycle_converted;
int32_t FREQUENCY = 10;

void run_pwm(float duty_cycle){
  /* Run PWM on a given pin at an input frequency and duty cycle.*/
  duty_cycle_converted = 255 * duty_cycle;
  analogWrite(PIN_PWM, duty_cycle_converted);
}

void stop_pwm(){
  /* Stop pwm on the pwm pin.*/
  //digitalWrite(PIN_PWM, LOW);
  digitalWrite(PIN_PWM, 0);
}


void setup() {
  // PWM Pin
  InitTimersSafe();
  bool success = SetPinFrequencySafe(PIN_PWM, FREQUENCY);
  pinMode(PIN_PWM, OUTPUT);
  // Pin indicating if PWM is running
  pinMode(PIN_RUNNING, OUTPUT);
  // Enable pin
  pinMode(PIN_ENABLE, INPUT_PULLUP);
  // Stop pwm if it was running
  stop_pwm();
}

void loop() {

  if (digitalRead(PIN_ENABLE)){
    if (!running){
      // Run PWM
      running = true;
      run_pwm(.5);
    }
  }
  else {
    stop_pwm();
    running = false;
  }
  digitalWrite(PIN_RUNNING, running);
  delay(1);
}
