#include <Wire.h>
#include <SSD1306Wire.h>

// install library ESP8266 for SSD1306

#include "my_wifi.h"
#include "my_light_sensor.h"

SSD1306Wire display(0x3c, 14, 12);  // using the built-in display

const int selectPins[3] = { D0, D1, D2 };  // S0~D0, S1~D1, S2~D2
const int zOutput = D8;                    // Connect common (Z) to D8 (PWM-capable)


void dispWiFiConfig() {
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawString(0, 0, "IP: " + WiFi.localIP().toString());
}

void selectMuxPin(byte pin) {
  if (pin > 7) return;  // Exit if pin is out of scope
  for (int i = 0; i < 3; i++) {
    if (pin & (1 << i))
      digitalWrite(selectPins[i], HIGH);
    else
      digitalWrite(selectPins[i], LOW);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println();

  display.init();
  display.clear();
  //display.flipScreenVertically(); // yellow line goes on top
  display.setFont(ArialMT_Plain_10);
  display.setTextAlignment(TEXT_ALIGN_LEFT);
  display.drawString(0, 0, "Connecting to Wi-Fi");
  display.display();
  
  connectToWiFi(120);
  dispWiFiConfig();
/*
  // The multiplexer part
  for (int i = 0; i < 3; i++) {
    pinMode(selectPins[i], OUTPUT);
    digitalWrite(selectPins[i], LOW);
  }
  pinMode(zOutput, OUTPUT);  // Set up Z as an output
  */
}

void loop() {
  //clear the display
  display.clear();
  dispWiFiConfig();

  int light = check_light_sensor();
  display.drawString(0, 14, "Light: ");
  display.drawString(60, 14, String(light));


  display.display();
  delay(1000);
}