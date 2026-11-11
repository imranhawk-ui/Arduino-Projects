#define JOYSTICK_X A0
#define JOYSTICK_Y A1
#define JOYSTICK_BTN 2
#define LED_PIN 8
bool ledState = false;
int lastButtonState = HIGH;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(4800);
  pinMode(JOYSTICK_BTN,INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int x_axis = analogRead(JOYSTICK_X);
  int y_axis = analogRead(JOYSTICK_Y);
  int State = digitalRead(JOYSTICK_BTN);

    if (lastButtonState == HIGH && State == LOW) {
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState ? HIGH : LOW);
  }

  lastButtonState = State;


  Serial.print("X AXIS: "); Serial.print(x_axis);
  Serial.print(" Y AXIS: "); Serial.print(y_axis);
  Serial.print(" BUTTON: "); Serial.println(State == LOW ? "Press" : "NOT PRESSED");

  delay(100);
}
