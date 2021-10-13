/*
  Use a serial port input to parametrize and run PWM on an arduino.
*/
// Define the parameters
#include <PWM.h>
#include "serial_helpers.h"
#define PIN_PWM 9
#define PIN_RUNNING 8
#define PIN_ENABLE 10
#define PIN_COUNTER 2
bool running = false;
bool order_computer = false;
bool received_parameters = false;
volatile bool detected_pulse = false;
int counter = 0;
int i;


void run_pwm(byte duty_cycle){
  /* Run PWM on a given pin at an input frequency and duty cycle.*/
  running = true;
  pwmWrite(PIN_PWM, duty_cycle);
}

void stop_pwm(){
  /* Stop pwm on the pwm pin.*/
  digitalWrite(PIN_PWM, LOW);
  counter = 0;
  running = false;
}

void callback_input_counter(){
  detected_pulse = true;
}

void blink_running_led(){
  for (i=0; i<5; i++){
    digitalWrite(PIN_RUNNING, HIGH);
    delay(100);
    digitalWrite(PIN_RUNNING, LOW);
    delay(100);
  }
}

void setup_pin_pwm(int32_t frequency){
  /* Setup of the PWM pin at a given frequency */
  InitTimersSafe();
  bool success = SetPinFrequencySafe(PIN_PWM, frequency);
  pinMode(PIN_PWM, OUTPUT);
}

void setup(){
  Serial.begin(9600);
  Serial.setTimeout(100);
  // Pin indicating if PWM is running
  pinMode(PIN_RUNNING, OUTPUT);
  // Enable pin
  pinMode(PIN_ENABLE, INPUT_PULLUP);
  // Counter pin
  pinMode(PIN_COUNTER, INPUT);
  attachInterrupt(digitalPinToInterrupt(PIN_COUNTER), callback_input_counter, RISING);
  // Blink the LED to confirm the arduino is ready for receiving the parameters
  blink_running_led();
  // Setup the PWM pin once the parameters are received
  while (!received_parameters){
    received_parameters = read_parameters();
    delay(1);
  }
  delay(100);
  setup_pin_pwm(FREQUENCY);
  stop_pwm();  // Stop pwm if it was running
  blink_running_led(); // blink the running LED to confirm setup is done
}

void pwm_loop_iteration(int chunk_size, byte duty_cycle, int interruption_time){
  // Handle interruptions when enough pulses were detected
  if (detected_pulse){
    counter += 1;
    detected_pulse = false;
  }
  if (chunk_size != 0 && counter >= 2 * chunk_size){
    stop_pwm();
    delay(interruption_time);
  }

  if (order_computer){
    order_computer = !read_stop();
  }
  else {
    order_computer = read_start();
  }

  if (digitalRead(PIN_ENABLE) && order_computer){
    if (!running){
      // Run PWM with the input duty cycle
      run_pwm(duty_cycle);
    }
  }
  else {
    stop_pwm();
  }
  digitalWrite(PIN_RUNNING, running);
  delay(1);
}

void loop(){
  pwm_loop_iteration(CHUNK_SIZE, DUTY_CYCLE, INTERRUPTION_TIME);
}
