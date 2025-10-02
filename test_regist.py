import RPi.GPIO as GPIO
import time
from random import choice, random

SDI   = 36
RCLK  = 40
SRCLK = 38
RESET = 32

def setup():
	GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
	GPIO.setup(SDI, GPIO.OUT)
	GPIO.setup(RCLK, GPIO.OUT)
	GPIO.setup(SRCLK, GPIO.OUT)
	GPIO.setup(RESET, GPIO.OUT)
	GPIO.output(SDI, GPIO.LOW)
	GPIO.output(RCLK, GPIO.LOW)
	GPIO.output(SRCLK, GPIO.LOW)

def shiftout(byte):
    print("---")
    for x in range(0,8):
        bit = (byte >> x) & 1
        print(bit)
        GPIO.output(SDI, bit)
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
    #print("pausa pre-accensione")
    #time.sleep(2)
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)
    print("pausa luci")
    time.sleep(2)

def reset():
    GPIO.output(RESET, GPIO.LOW)
    GPIO.output(RESET, GPIO.HIGH)

        
def destroy():   # When program ending, the function is executed. 
	GPIO.cleanup()


LINES = [128, 64, 32, 16, 8, 4, 2, 1]
ACTIVE = [1,3,5,7]


setup()
#reset()
#shiftout(0b00000001)
#reset()
#shiftout(0b00000010)
reset()
shiftout(0b11111111)
#reset()
#shiftout(0b00000111)

#reset()
#shiftout(LINES[1])
# reset()
# shiftout(LINES[3])
# reset()
# shiftout(LINES[5])
# reset()
# shiftout(LINES[7])
# reset()

#all off
reset()
shiftout(0b11111111)

destroy()