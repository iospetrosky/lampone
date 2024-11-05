int latchPin = D7; // L_Clock
int clockPin = D5; // Clock
int dataPin = D6; // Ser_in
//int resetPin = D2; 

/*
Map of the other pins
Reset: VCC - this MUST be connected
OE: ground - not relevant even if not connected
*/

byte leds = 0;
 
void setup() 
{
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);  
  pinMode(clockPin, OUTPUT);
  pinMode(resetPin, OUTPUT);

  digitalWrite(resetPin, LOW);
}
 
void loop() 
{
  leds = 0;
  updateShiftRegister();
  delay(200);
  
  for (int i = 0; i < 8; i++)
  {
    bitSet(leds, i);
    updateShiftRegister();
    
    delay(200);
  }
  for (int i = 0; i<20 ; i++) {
    leds = random(0,255);
    updateShiftRegister();
    delay(100);
  }
}
 
void updateShiftRegister()
{
   digitalWrite(latchPin, LOW);
   shiftOut(dataPin, clockPin, LSBFIRST, leds);
   digitalWrite(latchPin, HIGH);
}