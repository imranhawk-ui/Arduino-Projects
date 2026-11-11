
const int ledPins[] = {3, 4, 5, 6, 7};

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 5; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');

    if (data.length() == 5) {
      for (int i = 0; i < 5; i++) {
        digitalWrite(ledPins[i], data[i] == '1' ? HIGH : LOW);
      }
    }
  }
}
