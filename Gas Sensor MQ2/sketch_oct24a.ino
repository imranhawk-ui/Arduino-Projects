const int gasPin = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int gasValue = analogRead(gasPin);

  Serial.print("MQ-2 reading: ");
  Serial.println(gasValue);

  delay(1000);
}
