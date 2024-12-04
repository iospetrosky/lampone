#include <Wire.h>
#include <SSD1306Wire.h>

// install library ESP8266 for SSD1306

#include "my_wifi.h"
#include "my_analog_pin.h"
#include "myMuxReader.h"

const int relay_pin = D5;

SSD1306Wire display(0x3c, 14, 12);  // using the built-in display
myMuxReader mux (D0, D1, D2, A0);

void dispWiFiConfig() {
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawString(0, 0, "IP: " + WiFi.localIP().toString());
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("ciao");

  pinMode(analog_pin, INPUT);  // really necessary?
  pinMode(relay_pin, OUTPUT);
  digitalWrite(relay_pin, LOW);

  display.init();
  display.clear();
  display.flipScreenVertically();  // yellow line goes on top
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawString(0, 0, "Connecting to Wi-Fi");
  display.display();

  connectToWiFi(120);
  dispWiFiConfig();
  Serial.println("Setup completed");
  
}

void loop() {
  //clear the display
  display.clear();
  dispWiFiConfig();


  int light = mux.readAnalogChannel(1);
  display.drawString(0, 14, "Light: ");
  display.drawString(60, 14, String(light));
  Serial.println("Light: " + String(light));
  
  if (light > 200) {
    digitalWrite(relay_pin, LOW);
  } else {
    digitalWrite(relay_pin, HIGH);
  }
  

  int water = mux.readAnalogChannel(7);
  display.drawString(0, 28, "Moist: ");
  display.drawString(60, 28, String(water));
  Serial.println("Moist: " + String(water));



  display.display();
  delay(1000);
}