
const int photoPin = A0;
const int ledPin = 9;

int photoValue = 0;
int ledBrightness = 0;

void setup()
{
  pinMode(photoPin, INPUT);
  pinMode(ledPin, OUTPUT);

  Serial.begin(9600);
}

void loop()
{
  // Read light sensor
  photoValue = analogRead(photoPin);

  // Convert sensor reading (0-1023) to PWM (0-255)
  ledBrightness = map(photoValue, 0, 1023, 0, 255);

  // Control LED brightness
  analogWrite(ledPin, ledBrightness);

  // Display readings
  Serial.print("Light Sensor: ");
  Serial.print(photoValue);

  Serial.print(" | LED Brightness: ");
  Serial.println(ledBrightness);

  delay(100);
}
