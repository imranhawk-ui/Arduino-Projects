
#include <WiFiS3.h>

char ssid[] = "Redmi";
char pass[] = "12345678";

const int LED_PIN = 2;

WiFiServer server(80);

void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  Serial.println("Connecting to Wi-Fi...");

  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    delay(2000);
    Serial.println("Retrying...");
  }

  Serial.println("Wi-Fi connected!");

   // Wait for network configuration
  delay(3000);

  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.begin();
  Serial.println("Web server started!");

  Serial.println("Web server started!");
}

void loop() {

  WiFiClient client = server.available();

  if (client) {

    String request = client.readStringUntil('\r');
    client.flush();

    if (request.indexOf("GET /H") >= 0) {
      digitalWrite(LED_PIN, HIGH);
    }

    if (request.indexOf("GET /L") >= 0) {
      digitalWrite(LED_PIN, LOW);
    }

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("Connection: close");
    client.println();

    client.println("<html><body style='text-align:center;"
                   "font-family:Arial;'>");

    client.println("<h1>Arduino IoT LED Control</h1>");

    client.println("<h2>LED Controller</h2>");

    client.println("<a href='/H'>"
                   "<button style='padding:20px;'>"
                   "LED ON</button></a>");

    client.println("<br><br>");

    client.println("<a href='/L'>"
                   "<button style='padding:20px;'>"
                   "LED OFF</button></a>");

    client.println("</body></html>");

    delay(1);
    client.stop();
  }
}
