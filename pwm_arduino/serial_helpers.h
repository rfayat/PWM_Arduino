#ifndef serial_helpers
#define serial_helpers
int32_t FREQUENCY;  // Hz
byte DUTY_CYCLE; // 0-255, 128 corresponds to a 50% duty cycle
int CHUNK_SIZE;  // Number of PWM cycles before starting a pause
int INTERRUPTION_TIME; // duration of the pauses, ms
String header;

void write_string(String string){
  for(auto c: string){
    Serial.write(c);
  }
  Serial.write('\n');
}

bool read_parameters(){
  if (Serial.available()){
    header = Serial.readStringUntil('\n');
    if (header == "parameters"){
      FREQUENCY = Serial.readStringUntil('\n').toInt();
      DUTY_CYCLE = Serial.readStringUntil('\n').toInt();
      CHUNK_SIZE = Serial.readStringUntil('\n').toInt();
      INTERRUPTION_TIME = Serial.readStringUntil('\n').toInt();
      Serial.write(DUTY_CYCLE);
      write_string("success");
      return true;
    }
    else {
      Serial.flush();
      return false;
    }
  }
  else {
    return false;
  }
}


#endif
