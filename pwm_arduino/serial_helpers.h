#ifndef serial_helpers
#define serial_helpers
int32_t FREQUENCY;  // Hz
byte DUTY_CYCLE; // 0-255, 128 corresponds to a 50% duty cycle
int CHUNK_SIZE;  // Number of PWM cycles before starting a pause
int INTERRUPTION_TIME; // duration of the pauses, ms
String header;

bool read_parameters(){
  if (Serial.available()){
    header = Serial.readStringUntil('\n');
    if (header == "parameters"){
      FREQUENCY = Serial.readStringUntil('\n').toInt();
      DUTY_CYCLE = Serial.readStringUntil('\n').toInt();
      CHUNK_SIZE = Serial.readStringUntil('\n').toInt();
      INTERRUPTION_TIME = Serial.readStringUntil('\n').toInt();
      Serial.write("success\n");
      return true;
    }
    else {
      Serial.flush();
      Serial.write("failure\n");
      return false;
    }
  }
  else {
    return false;
  }
}

bool read_start(){
  if (Serial.available()){
    header = Serial.readStringUntil('\n');
    if (header == "start"){
      Serial.write("success\n");
      return true;
    }
    else {
      Serial.flush();
      Serial.write("failure\n");
      return false;
    }
  }
  else {
    return false;
  }
}

bool read_stop(){
  if (Serial.available()){
    header = Serial.readStringUntil('\n');
    if (header == "stop"){
      Serial.write("success\n");
      return true;
    }
    else {
      Serial.flush();
      Serial.write("failure\n");
      return false;
    }
  }
  else {
    return false;
  }
}

#endif
