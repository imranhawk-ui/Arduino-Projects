const int irPin = 7;

void setup() {
  pinMode(irPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  int value = digitalRead(irPin);

  if (value == LOW) {
    Serial.println("No object");
  } else {
    Serial.println("Object detected!");
  }

  delay(300);
}
