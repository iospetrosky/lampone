// This sketch works for any NodeMCU controller

#define P1 D5
#define P2 D6
#define P3 D7
#define P4 D8
#define PAUSA 200

void setup()
{
    // initialize digital pin LED_BUILTIN as an output.
    pinMode(P1, OUTPUT);
    pinMode(P2, OUTPUT);

    pinMode(P3, OUTPUT);
    pinMode(P4, OUTPUT);
}

// the loop function runs over and over again forever
void loop()
{
    digitalWrite(P1, HIGH); // turn the LED on (HIGH is the voltage level)
    delay(PAUSA);           // wait for a second
    digitalWrite(P2, HIGH); // turn the LED on (HIGH is the voltage level)
    delay(PAUSA);           // wait for a second
    digitalWrite(P3, HIGH); // turn the LED on (HIGH is the voltage level)
    delay(PAUSA);           // wait for a second
    digitalWrite(P4, HIGH); // turn the LED on (HIGH is the voltage level)
    delay(PAUSA);           // wait for a second
    digitalWrite(P1, LOW);  // turn the LED on (HIGH is the voltage level)
    delay(PAUSA);           // wait for a second
    digitalWrite(P2, LOW);  // turn the LED on (HIGH is the voltage level)
    delay(PAUSA);           // wait for a second
    digitalWrite(P3, LOW);  // turn the LED on (HIGH is the voltage level)
    delay(PAUSA);           // wait for a second
    digitalWrite(P4, LOW);  // turn the LED on (HIGH is the voltage level)
    delay(PAUSA);           // wait for a second
}
