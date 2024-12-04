class myMuxReader {
private:
  int pins[3] = {0,0,0};
  int analogPin = 0;

  void selectMuxPin(byte pin) {
    if (pin > 7) return;  // Exit if pin is out of scope
    for (int i = 0; i < 3; i++) {
      if (pin & (1 << i))
        digitalWrite(pins[i], HIGH);
      else
        digitalWrite(pins[i], LOW);
    }
  }

public:
  myMuxReader(int S0, int S1, int S2, int AnInp) {
    pins[0] = S0;
    pins[1] = S1;
    pins[2] = S2;
    pinMode(S0, OUTPUT);
    digitalWrite(S0, LOW);
    pinMode(S1, OUTPUT);
    digitalWrite(S1, LOW);
    pinMode(S2, OUTPUT);
    digitalWrite(S2, LOW);
    analogPin = AnInp;
  }

  int readAnalogChannel(byte C) {
    selectMuxPin(C);
    for (int i = 0; i < 10; i++) {
      analogRead(analogPin);  // dummy read to throw away fake reading
      delay(100);
    }
    return analogRead(analogPin);
  }
};
