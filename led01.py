from gpiozero import LED
from time import sleep

led = LED(25)
k = 0
while k < 5:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    k = k +1
