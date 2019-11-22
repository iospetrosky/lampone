import RPi.GPIO as GPIO
import time

SDI   = 11
RCLK  = 12
SRCLK = 13
RESET = 7

#Q0 is the leftmost bit
LINE01 = 128 #Q0
LINE02 = 64  #Q1
LINE03 = 32  #etc.

matrix = 0  #this is the light matrix, the byte to be pushed

def intro_msg():
	print ('Program is running...')
	print ('Please press Ctrl+C to end the program...')

def setup():
    GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    GPIO.setup(RESET, GPIO.OUT)
    GPIO.output(SDI, GPIO.LOW)
    GPIO.output(RCLK, GPIO.LOW)
    GPIO.output(SRCLK, GPIO.LOW)

def lights_on(line):
    global matrix
    matrix = matrix + line
    hc595_in(matrix)    

def lights_off(line):
    global matrix
    matrix = matrix - line
    hc595_in(matrix)    
    
def hc595_push(dat):
    print("Pushing {}".format(dat))
    for bit in range(0, 8):
        b = (dat >> bit) & 1
        print(b)
        GPIO.output(SDI, b )
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
 
def hc595_go():
	GPIO.output(RCLK, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(RCLK, GPIO.LOW)

def hc595_reset():
    GPIO.output(RESET, GPIO.LOW)
    GPIO.output(RESET, GPIO.HIGH)

def loop():
    while True:
        reset()


def destroy():   # When program ending, the function is executed. 
	GPIO.cleanup()

if __name__ == '__main__': # Program starting from here 
    print_msg()
    setup() 
    try:
        loop()  
    except KeyboardInterrupt:  
        print("Exiting")  
    destroy()
