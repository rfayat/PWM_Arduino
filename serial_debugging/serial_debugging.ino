#define PIN_RUNNING 8
int i;
String incoming;

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

void loop(){
  delay(100);
  while (Serial.available()){
    incoming = Serial.readStringUntil('\n');
    write_string(incoming);
  }
}
