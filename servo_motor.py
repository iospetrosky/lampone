import RPi.GPIO as GPIO
import time, signal, sys



servoPIN = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) 
p.start(2.5) # Initialization
try:
    while True:
        print("Cycle")
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(12.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(0.5)
        p.ChangeDutyCycle(7.5)
        time.sleep(0.5)
        p.ChangeDutyCycle(5)
        time.sleep(0.5)
        p.ChangeDutyCycle(2.5)
        time.sleep(0.5)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
