#include <DHT.h>

// Define the DHT11 pin and type
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

double temp = 0;

void setup()
{
  Serial.begin(9600);
  dht.begin(); // Start the DHT11
  
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(3, OUTPUT);
}

void loop()
{
  // Read temperature as Celsius
  float t = dht.readTemperature();
  float h = dht.readHumidity();
 
  // Check if the sensor is working
  if (isnan(t)||isnan(h)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  temp = t; // Convert the float reading to an integer for your original code
  Serial.println(temp);
  Serial.println(h);
  // --- YOUR ORIGINAL LED LOGIC (UNCHANGED) ---
  if (temp < 25.00) {
    digitalWrite(5, HIGH);
    digitalWrite(4, LOW);
    digitalWrite(3, LOW);
  }
  if (temp >25.00 && temp <28.00) {
    digitalWrite(5, LOW);
    digitalWrite(4, HIGH);
    digitalWrite(3, LOW);
  }
  if (temp > 28.00) {
    digitalWrite(5, LOW);
    digitalWrite(4, LOW);
    digitalWrite(3, HIGH);
  }
  
  delay(2000); // Changed from 10ms to 2000ms because DHT11 needs 2 seconds between reads
}
