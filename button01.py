from gpiozero import LED, Button
from time import sleep

led = LED(17)
button = Button(2)

button.wait_for_press()
led.on()
sleep(3)
led.off()

#this toggles the led
while True:
    button.wait_for_press()
    led.toggle()
    sleep(0.5)
