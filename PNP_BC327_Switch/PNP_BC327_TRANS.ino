
const int transistorPin = 8;
const int onButton = 2;
const int offButton = 3;

void setup() {
  pinMode(transistorPin, OUTPUT);
  pinMode(onButton, INPUT_PULLUP);
  pinMode(offButton, INPUT_PULLUP);

  // PNP transistor OFF
  digitalWrite(transistorPin, HIGH);
}

void loop() {
  if (digitalRead(onButton) == LOW) {
    digitalWrite(transistorPin, LOW);   // ON
  }

  if (digitalRead(offButton) == LOW) {
    digitalWrite(transistorPin, HIGH);  // OFF
  }
}
