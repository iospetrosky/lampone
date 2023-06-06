import time
import RPi.GPIO as GPIO

relay_pin = 37

# this explains the matter very well
# https://www.circuitbasics.com/setting-up-a-5v-relay-on-the-arduino/

GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay_pin, GPIO.OUT)

def destroy():
    # set to HIGH to switch  the relay to NC
    GPIO.output(relay_pin,GPIO.HIGH)    
    print("Switched to NC")
    GPIO.cleanup()                     # Release resource
    
try:
    while True:
             GPIO.output(relay_pin,GPIO.LOW) #switch to NO
             print("Switched to NO")
             time.sleep(5)
             GPIO.output(relay_pin,GPIO.HIGH) #switch to NC
             print("Switched to NC")
             time.sleep(5)

except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
    destroy()
