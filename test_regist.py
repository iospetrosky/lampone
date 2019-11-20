import RPi.GPIO as GPIO
import time

SDI   = 11
RCLK  = 12
SRCLK = 13
RESET = 7

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
    print("pausa pre-accensione")
    time.sleep(2)
    GPIO.output(RCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)
    print("pausa luci on")
    time.sleep(2)

def reset():
    GPIO.output(RESET, GPIO.LOW)
    GPIO.output(RESET, GPIO.HIGH)

        
def destroy():   # When program ending, the function is executed. 
	GPIO.cleanup()
        
setup()
reset()
shiftout(0b11100000)
reset()
shiftout(0b10000000)
reset()
shiftout(0b01000000)
reset()
shiftout(0b00100000)
destroy()