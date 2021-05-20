##micro python - for micro:bit
from microbit import *
from machine import time_pulse_us
trig = pin6
echo = pin7
display.off() ## otherwise I can't use the pins above
trig.write_digital(0)
echo.read_digital()
while True:
    trig.write_digital(1)
    trig.write_digital(0)
    micros = time_pulse_us(echo, 1) 
    t_echo = micros / 1000000
    dist_cm = (t_echo / 2) * 34300
    display.on()
    display.scroll(str(int(dist_cm)))
    display.off()
    sleep(100)