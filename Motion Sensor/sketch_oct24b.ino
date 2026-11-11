const int motionPin = 2;

void setup() {
  pinMode(motionPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  int motion = digitalRead(motionPin);

  if (motion == HIGH) {
    Serial.println("Motion detected!");
  } else {
    Serial.println("No motion");
  }

  delay(500);
}
