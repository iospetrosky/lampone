from gpiozero import LED, Button
from time import sleep

green = LED(4)
yellow = LED(26)
button = Button(21)

button.wait_for_press()
print("Button pressed")
green.on()
sleep(3)
green.off()

#this toggles the led
while True:
    button.wait_for_press()
    yellow.toggle()
    sleep(0.5)
