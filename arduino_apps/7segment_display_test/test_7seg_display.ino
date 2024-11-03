// This sketch works for any NodeMCU controller
#define PAUSA 1000

int pins[] = { D1, D7 };
int pin_count = 2;

void welcome_blink() {
  for (int x = 0; x < 6; x++) {
    digitalWrite(D4, LOW);
    delay(500);
    digitalWrite(D4, HIGH);
    delay(500);
  }
}

void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(D4, OUTPUT);
  // put all the pins to HIGH
  // since this is Anode common
  for (int x = 0; x < pin_count; x++) {
    pinMode(pins[x], OUTPUT);
    digitalWrite(pins[x], HIGH);
  }
  welcome_blink();
}

// the loop function runs over and over again forever
void loop() {
  for (int x = 0; x < pin_count; x++) {
    digitalWrite(pins[x], LOW);
    delay(PAUSA);
    digitalWrite(pins[x], HIGH);
    delay(PAUSA);
  }
}
