import RPi.GPIO as GPIO
import time, signal, sys, json
from random import choice, random

SDI   = 11 #serial input
RCLK  = 12 #serial push
SRCLK = 13 #activation 
RESET = 7  #reset

#Q0 is the leftmost bit
LINES = [128, 64, 32, 16, 8, 4, 2, 1]
ACTIVE = [0,1,2]

matrix = 0  #this is the light matrix, the byte to be pushed

def terminateProcess(signalNumber, frame):
    print ('Program killed')
    hc595_reset()
    destroy()
    sys.exit()

def intro_msg():
	print ('Program is running...')
	print ('Press Ctrl+C to end the program...')

def setup():
    f = open("/home/pi/WWW/lampone/lights.json","w")
    f.write("fake file to cause an error")
    f.close()
    GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    GPIO.setup(RESET, GPIO.OUT)
    GPIO.output(SDI, GPIO.LOW)
    GPIO.output(RCLK, GPIO.LOW)
    GPIO.output(SRCLK, GPIO.LOW)
    GPIO.output(RESET, GPIO.LOW)
    signal.signal(signal.SIGTERM, terminateProcess)

def lights_on(line):
    global matrix
    print("Switching light: {} -- ON".format(line))
    matrix = matrix | line
    hc595_push(matrix)    
    hc595_go()

def lights_off(line):
    global matrix
    print("Switching light: {} -- OFF".format(line))
    if ((matrix & line) == line):
        matrix = matrix - line
    hc595_push(matrix)    
    hc595_go()

def lights_switch(line):
    if ((matrix & line) == line):
        lights_off(line)
    else:
        lights_on(line)

def hc595_push(dat):
    print("Pushing {}".format(dat))
    for bit in range(0, 8):
        b = (dat >> bit) & 1
        #print(b)
        GPIO.output(SDI, b )
        GPIO.output(SRCLK, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)
 
def hc595_go():
	GPIO.output(RCLK, GPIO.HIGH)
	time.sleep(0.001)
	GPIO.output(RCLK, GPIO.LOW)

def hc595_reset():
    GPIO.output(RESET, GPIO.HIGH) 
    time.sleep(0.01)    
    GPIO.output(RESET, GPIO.LOW)


def loop():
    last_stamp = 0
    time.sleep(0.5)
    while True:
        try:
            data = json.load(open("/home/pi/WWW/lampone/lights.json"))
            if (data['stamp'] != last_stamp):
                last_stamp = data['stamp']
                hc595_reset()
                #select one of the active lights to play with
                if (data['mode'] == 'off'):
                    lights_off(int(data['light'])) 
                if (data['mode'] == 'on'):
                    lights_on(int(data['light'])) 
        except:
            print("Some problem with the json file")
            time.sleep(1)
            
def destroy():   # When program ending, the function is executed. 
	GPIO.cleanup()

if __name__ == 'zz__main__': # Program starting from here 
    setup() 
    hc595_reset()
    hc595_push(0)
    hc595_go()
    hc595_reset()
    destroy()
    
    
if __name__ == '__main__': # Program starting from here 
    intro_msg()
    setup() 
    try:
        loop()  
    except KeyboardInterrupt:  
        print("Exiting")  
    hc595_reset()
    destroy()
