#define PIN_RUNNING 8
int i;
String header;
bool received_parameters = false;
int32_t FREQUENCY;  // Hz
byte DUTY_CYCLE; // 0-255, 128 corresponds to a 50% duty cycle
int CHUNK_SIZE;  // Number of PWM cycles before starting a pause
int INTERRUPTION_TIME; // duration of the pauses, ms


void blink_running_led(){
  for (i=0; i<10; i++){
    digitalWrite(PIN_RUNNING, HIGH);
    delay(100);
    digitalWrite(PIN_RUNNING, LOW);
    delay(100);
  }
}

void write_string(String string){
  for(auto c: string){
    Serial.write(c);
  }
  Serial.write('\n');
}

void setup(){
  Serial.begin(9600);
  Serial.setTimeout(100);
  pinMode(PIN_RUNNING, OUTPUT);
  blink_running_led();
}

bool read_parameters(){
  if (Serial.available()){
    header = Serial.readStringUntil('\n');
    if (header == "parameters"){
      FREQUENCY = Serial.readStringUntil('\n').toInt();
      DUTY_CYCLE = Serial.readStringUntil('\n').toInt();
      CHUNK_SIZE = Serial.readStringUntil('\n').toInt();
      INTERRUPTION_TIME = Serial.readStringUntil('\n').toInt();
      write_string("success");
      blink_running_led();
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

void loop(){
  received_parameters = false;
  while (!received_parameters){
    received_parameters = read_parameters();
  }
  delay(100);
}
