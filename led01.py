import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)      # Use BCM pin numbering
GPIO.setup(25, GPIO.OUT)    # Set GPIO 25 as output

for i in range(5):
    GPIO.output(25, GPIO.HIGH)  # Turn LED on
    time.sleep(1)
    GPIO.output(25, GPIO.LOW)   # Turn LED off
    time.sleep(1)

GPIO.cleanup()              # Reset GPIO state