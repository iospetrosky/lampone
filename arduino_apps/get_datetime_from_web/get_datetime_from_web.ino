#include "arduino_secrets.h"

#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>

#define DEBUG 1  // comment out to disable debug messages

int d_led = D8;

void setup() {
    Serial.begin(9600);
    pinMode(d_led, OUTPUT);

    digitalWrite(d_led, LOW);
    connect_to_wifi(D8);
}

void loop() {
    String dt = get_datetime_from_web();
    delay(1000);
}

void blink_times(int led_num, int times, int interval) {
    for (int x = 0; x < times; x++) {
        digitalWrite(led_num, HIGH);  // this swithes on
        delay(interval);
        digitalWrite(led_num, LOW);  // this swithes off
        delay(interval);
    }
}

const char* ssid = "lorenzo_work24";  // network ID
const char* password = "f3d3r1c0";
void connect_to_wifi(int sig_led) {
    Serial.println("Connecting to WiFi");
    WiFi.begin(ssid, password);
    int k = 0;
    while (WiFi.status() != WL_CONNECTED) {
        digitalWrite(sig_led, HIGH);
        delay(200);
        digitalWrite(sig_led, LOW);
        delay(200);
        k++;
        if (k > 30) {
            Serial.println("WiFi not connecting - forced restart");
            ESP.restart();
        }
    }

    // Print the IP address
    Serial.println(WiFi.localIP());
    blink_times(sig_led, 10, 30);
}

String get_datetime_from_web() {
    // const char* host = "httpbin.org";
    const char* host = "timeapi.io";
    // String url = "/get";
    String url = "/api/Time/current/zone?timeZone=Europe/London";

    WiFiClientSecure client;

    client.setInsecure();
    if (!client.connect(host, 443)) {  // 443 is the https port
        Serial.println("Connect to host failure");
        return "0000-00-00 00:00:00";
    }

    client.print(String("GET ") + url + " HTTP/1.1\r\n" + "Host: " + host +
                 "\r\n" + "Connection: close\r\n\r\n");
#ifdef DEBUG
    Serial.println("request sent");
#endif
    while (client.connected()) {
        String line = client.readStringUntil('\n');
#ifdef DEBUG
        Serial.println(line);
#endif
        if (line == "\r") {
#ifdef DEBUG
            Serial.println("headers received");
#endif
            break;
        }
    }

    String chunk = "";
    int limit = 1;
    String response = "";

    /* it could be a little more clever, but I read until I find a chunk
       starting with a { I keep that chunk and terminate the transfer */
    do {
        if (client.connected()) {
            client.setTimeout(2000);
            chunk = client.readStringUntil('\n');
#ifdef DEBUG
            Serial.println(chunk);
#endif
            if (chunk.startsWith("{")) {
                response = chunk;
                break;
            }
        }
    } while (chunk.length() > 0 && ++limit < 100);
#ifdef DEBUG
    Serial.println("==========");
    Serial.println(response);
    Serial.println("==========");
#endif
    int dtpos = response.indexOf("dateTime") + 11;
    String dtext = response.substring(dtpos, dtpos + 19);
    dtext.replace("T", " ");
    return dtext;
}