import RPi.GPIO as GPIO
import time, signal, sys, datetime
from random import choice, random, randint
import json

SDI   = 40 #serial input
RCLK  = 38 #serial push
SRCLK = 36 #activation 
RESET = 32  #reset

#Q0 is the leftmost bit
LINES = [128, 64, 32, 16, 8, 4, 2, 1]
#A = 0, H = 7
ACTIVE = [1,3,5,7]

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
    GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    GPIO.setup(RESET, GPIO.OUT)
    GPIO.output(SDI, GPIO.LOW)
    GPIO.output(RCLK, GPIO.LOW)
    GPIO.output(SRCLK, GPIO.LOW)
    signal.signal(signal.SIGTERM, terminateProcess)

def lights_on(line):
    global matrix
    print("Switching light: {} -- ON".format(line))
    matrix = matrix + line
    #hc595_reset()
    hc595_push(matrix)    
    hc595_go()

def lights_off(line):
    global matrix
    print("Switching light: {} -- OFF".format(line))
    matrix = matrix - line
    #hc595_reset()
    hc595_push(matrix)    
    hc595_go()

def lights_all_off():
    global matrix
    matrix = 0
    hc595_push(0)
    hc595_go()

def lights_all_on():
    hc595_push(255)
    hc595_go()

def lights_switch(line):
    if ((matrix & line) == line):
        lights_off(line)
    else:
        lights_on(line)

def single_bit_push(b):
    print("Single push {}".format(b))
    GPIO.output(SDI, b )
    GPIO.output(SRCLK, GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(SRCLK, GPIO.LOW)
    hc595_go()


def hc595_push(dat):
    print("Pushing {}".format(dat))
    for bit in range(0, 8):
        b = (dat >> bit) & 1
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
    time.sleep(0.01)    
    GPIO.output(RESET, GPIO.HIGH)


def loop():
    web_switch = False 
    jsonfile = "/home/pi/WWW/lampone/web_switch.json"
    while True:
        time.sleep(0.5)
        #open json file and check if the switch is active
        try:
            data = json.load(open(jsonfile))
            if (data["manual"] == "auto"):
                now = datetime.datetime.now()
                t1 = data["next_on"].split(":")
                t2 = data["next_off"].split(":")
                if (now.hour >= int(t1[0])) and (now.minute >= int(t1[1])) and (data["mode"] == "off"):
                    data["mode"] = "on"
                    json.dump(data, open(jsonfile,"w"))
                if (now.hour >= int(t2[0])) and (now.minute >= int(t2[1])) and (data["mode"] == "on"):
                    data["mode"] = "off"
                    json.dump(data, open(jsonfile,"w"))
            if (data['mode'] == 'off'):
                web_switch = False 
            if (data['mode'] == 'on'):
                web_switch = True
        except:
            print("Error loading JSON")
            web_switch = False

        if web_switch:
            setup()
            sleep_interval = randint(20,300) / 1000
            for j in range(0,100):
                single_bit_push(randint(0,1))
                time.sleep(sleep_interval)
            #hc595_reset()
            for j in range(0,5):
                lights_all_on()
                time.sleep(sleep_interval)
                lights_all_off()
                time.sleep(0.2)
            destroy()
        else:
            print("Tree is off")
            #lights_all_off()
            #hc595_reset()

def destroy():   # When program ending, the function is executed. 
    hc595_push(0)
    hc595_go()
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
    #setup() 
    try:
        loop()  
    except KeyboardInterrupt:  
        print("Exiting")  
    hc595_reset()
    lights_all_off()

    destroy()
