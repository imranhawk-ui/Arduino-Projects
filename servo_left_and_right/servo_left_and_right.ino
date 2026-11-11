
#include <Servo.h>

Servo myServo;

const int SERVO_PIN = 9;
const int LEFT_BUTTON = 2;
const int RIGHT_BUTTON = 3;

int angle = 0;

void setup() {
  pinMode(LEFT_BUTTON, INPUT_PULLUP);
  pinMode(RIGHT_BUTTON, INPUT_PULLUP);

  myServo.attach(SERVO_PIN);
  myServo.write(angle);
}

void loop() {
  // Button 1: decrease angle
  if (digitalRead(LEFT_BUTTON) == LOW) {
    delay(30);  // Debounce

    if (digitalRead(LEFT_BUTTON) == LOW) {
      angle -= 15;

      if (angle < 0) {
        angle = 0;
      }

      myServo.write(angle);

      // Wait for button release
      while (digitalRead(LEFT_BUTTON) == LOW) {
        delay(10);
      }
      delay(30);
    }
  }

  // Button 2: increase angle
  if (digitalRead(RIGHT_BUTTON) == LOW) {
    delay(30);  // Debounce

    if (digitalRead(RIGHT_BUTTON) == LOW) {
      angle += 15;

      if (angle > 180) {
        angle = 180;
      }

      myServo.write(angle);

      // Wait for button release
      while (digitalRead(RIGHT_BUTTON) == LOW) {
        delay(10);
      }
      delay(30);
    }
  }
}
