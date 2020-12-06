import RPi.GPIO as GPIO
import time, signal, sys
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
    while True:
        time.sleep(2)
        #open json file and check if the switch is active
        try:
            data = json.load(open("/home/pi/WWW/lampone/web_switch.json"))
            if (data['mode'] == 'off'):
                web_switch = False 
            if (data['mode'] == 'on'):
                web_switch = True
        except:
            print("Error loading JSON")
            web_switch = False

        if web_switch:
            #when motion is detected the lights go for a while
            #select the kind of effects
            game = randint(1,3)
            data['game'] = game
            json.dump(data, open("/home/pi/WWW/lampone/web_switch.json","w"))
            if (game == 1):
                print("Game 1 - random lights")
                lights_all_off()
                for iter in range(0,10):
                    print ("Iteration {}".format(iter))
                    #select one of the active lights to play with
                    lights_switch(LINES[choice(ACTIVE)]) 
                    time.sleep(random() + 0.3)
            if (game == 2):
                print("Game 2 - circle lights")
                for iter in range(0,10):
                    print ("Iteration {}".format(iter))
                    lights_all_off()
                    hc595_reset()
                    for lg in ACTIVE:
                        #hc595_reset()
                        lights_on(LINES[lg])
                        time.sleep(1)
                        lights_off(LINES[lg])
            if (game == 3):
                print ("Game 3 - intermittent all lights")
                intermittence = randint(50,400) / 1000
                for iter in range(0,10):
                    print ("Iteration {}".format(iter))
                    hc595_reset()
                    lights_all_off()
                    time.sleep(intermittence)
                    lights_all_on()
                    time.sleep(intermittence)
        else:
            print("Tree is off")
            lights_all_off()
            hc595_reset()

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
    setup() 
    try:
        loop()  
    except KeyboardInterrupt:  
        print("Exiting")  
    hc595_reset()
    lights_all_off()

    destroy()
