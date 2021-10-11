/*
  Use a serial port input to parametrize and run PWM on an arduino.
*/
// Define the parameters
#include <PWM.h>
#define PIN_PWM 9
#define PIN_RUNNING 8
#define PIN_ENABLE 10
#define PIN_COUNTER 2
bool running = false;
byte duty_cycle_converted;
int32_t FREQUENCY = 10;
const int CHUNK_SIZE = 50;
volatile bool detected_pulse = false;
int counter = 0;
int interruption_time = 1000; // ms

void run_pwm(float duty_cycle){
  /* Run PWM on a given pin at an input frequency and duty cycle.*/
  running = true;
  duty_cycle_converted = 255 * duty_cycle;
  analogWrite(PIN_PWM, duty_cycle_converted);
}

void stop_pwm(){
  /* Stop pwm on the pwm pin.*/
  //digitalWrite(PIN_PWM, LOW);
  digitalWrite(PIN_PWM, 0);
  counter = 0;
  running = false;
}

void callback_input_counter(){
  detected_pulse = true;
  Serial.print("tartiflette ");
}

void setup() {
  Serial.begin(9600);
  // PWM Pin
  InitTimersSafe();
  bool success = SetPinFrequencySafe(PIN_PWM, FREQUENCY);
  pinMode(PIN_PWM, OUTPUT);
  // Pin indicating if PWM is running
  pinMode(PIN_RUNNING, OUTPUT);
  // Enable pin
  pinMode(PIN_ENABLE, INPUT_PULLUP);
  // Counter pin
  pinMode(PIN_COUNTER, INPUT);
  attachInterrupt(digitalPinToInterrupt(PIN_COUNTER), callback_input_counter, FALLING);
  // Stop pwm if it was running
  stop_pwm();
}

void loop() {
  if (detected_pulse){
    counter += 1;
    detected_pulse = false;
  }
  if (counter >= CHUNK_SIZE){
    stop_pwm();
    delay(interruption_time);
  }

  if (digitalRead(PIN_ENABLE)){
    if (!running){
      // Run PWM
      run_pwm(.5);
    }
  }
  else {
    stop_pwm();
  }
  digitalWrite(PIN_RUNNING, running);
  delay(1);
}
