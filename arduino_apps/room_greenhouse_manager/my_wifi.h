#include <ESP8266WiFi.h>

const char *ssid = "lorenzo_work24";
const char *password = "f3d3r1c0";

void connectToWiFi(int host_number = 0) {
  if (host_number > 0) {
    IPAddress subnet(255, 255, 255, 0);
    IPAddress gateway(192, 168, 1, 254);
    IPAddress local_IP(192, 168, 1, host_number);
    if (WiFi.config(local_IP, gateway, subnet)) {
      Serial.println("Static IP Configured");
    } else {
      Serial.println("Static IP Configuration Failed");
    }
  }
  WiFi.begin(ssid, password);
  // Initialising the UI will init the display too.
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Attempting to connect to WiFi");
    delay(500);
  }
}