#!/usr/bin/env python3
########################################################################
# Filename    : UltrasonicRanging.py
# Description : Get distance from UltrasonicRanging.
# Author      : freenove
# modification: 2018/08/03
########################################################################
import RPi.GPIO as GPIO
import time

trigPin = 4
echoPin = 17
MAX_DISTANCE = 220          #define the maximum measured distance
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance

leds = [4,25,21]
buzz = 24



def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime
    
def getSonar():     #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      #make trigPin send 10us high level 
    time.sleep(0.00001)     #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # the sound speed is 340m/s, and calculate distance
    return distance
    
def setup():
    print ('Program is starting...')
    GPIO.setmode(GPIO.BCM)       #numbers GPIOs by physical location
    GPIO.setup(trigPin, GPIO.OUT)   #
    GPIO.setup(echoPin, GPIO.IN)    #
    GPIO.setup(buzz, GPIO.OUT)    #
    for ledPin in leds:
        GPIO.setup(ledPin, GPIO.OUT)

def green_blink(tt):
    GPIO.output(buzz,GPIO.HIGH) #buzz
    time.sleep(tt)
    GPIO.output(buzz,GPIO.LOW) #buzz


def loop():
    GPIO.setup(11,GPIO.IN)
    while(True):
        distance = getSonar()
        print ("The distance is : %.2f cm"%(distance))
        bl = 0
        if distance < 20:
            leds_on(0)
            bl = 0.05
        else:
            leds_off(0)

        if distance < 40:
            leds_on(1)
            bl = 0.1
        else:
            leds_off(1)

        if distance < 60:
            leds_on(2)
            bl = 0.2
        else:
            leds_off(2)

        if distance > 60:
            all_off()
        else:
            green_blink(bl)

        time.sleep(0.1)


def all_off():
    for ledPin in leds:
        GPIO.output(ledPin, GPIO.LOW)

def leds_on(pin):
    GPIO.output(leds[pin], GPIO.HIGH)        

def leds_off(pin):
    GPIO.output(leds[pin], GPIO.LOW)        

        
if __name__ == '__main__':     #program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:  #when 'Ctrl+C' is pressed, the program will exit
        GPIO.cleanup()         #release resource
