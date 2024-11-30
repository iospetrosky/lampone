const int light_pin = A0; // the analog pin

int check_light_sensor()  {
    return  analogRead(light_pin);
}