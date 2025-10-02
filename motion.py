import RPi.GPIO as GPIO
import time

led_pin = 40
sens_pin = 16

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(led_pin, GPIO.OUT)   # Set ledPin's mode is output
    GPIO.output(led_pin, GPIO.LOW)  # Set ledPin low to off led
    GPIO.setup(sens_pin, GPIO.IN)
    time.sleep(2)
    print ('using pin %d for led'%led_pin)
    print ('using pin %d for sensor'%sens_pin)

def destroy():
    GPIO.output(led_pin, GPIO.LOW)     # led off
    GPIO.cleanup()                     # Release resource
    

setup()

try:
    while True:
        if (GPIO.input(sens_pin)):
            print("Motion")
            GPIO.output(led_pin,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(led_pin,GPIO.LOW)
except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()