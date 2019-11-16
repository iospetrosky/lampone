import time
import RPi.GPIO as GPIO

sens_pin = 17
relay_pin = 18


GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(sens_pin, GPIO.IN)

def destroy():
    GPIO.output(relay_pin,GPIO.HIGH)    
    GPIO.cleanup()                     # Release resource
    
try:
    while True:
        if (GPIO.input(sens_pin)):
            print("Motion")
            GPIO.output(relay_pin,GPIO.LOW)
            time.sleep(5)
            GPIO.output(relay_pin,GPIO.HIGH)
            time.sleep(5)
            print("Sensing motion again")
except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()
