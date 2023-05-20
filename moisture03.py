#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import smtplib # This is the SMTP library we need to send the email notification
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

#calculate the charge time of the capacitor
def rc_time (pin):
    count = 0
    #Output on the pin for 
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    #Change the pin back to input
    GPIO.setup(pin, GPIO.IN)
    #Count until the pin goes high
    while (GPIO.input(pin) == GPIO.LOW):
        count += 1
    return count

## send the notification via email
def sendmail(subject, text_message):
    smtp_username = "loruk371@gmail.com" 
    smtp_password = "tiudnygltapfymks" 

    #smtp_username = "lorenzo.pedrotti@gmail.com" 
    #smtp_password = "faiahpuwljyhrhxn" 

    receiver_address = 'lorenzo.pedrotti@gmail.com'

    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = receiver_address
    message['Subject'] = subject

    message.attach(MIMEText(text_message, 'plain'))

    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(smtp_username, smtp_password) #login with mail_id and password
    text = message.as_string()
    session.sendmail(smtp_username, receiver_address, text)
    session.quit()

dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

moist_pins = [8,16]
light_pin = 29
LIGHT_TRESHOLD = 1000 # higher means darker 
relay_pins = [7,11] # of the moist sensors, the last is the light switch
pots = ['Strawberry','Ivy']

# returns 0 when the moisture led is on meaning that the soil
# is moist enough - when it turns to 1 it means watering is needed
GPIO.setmode(GPIO.BOARD) # phisical bnoard

GPIO.setup(moist_pins, GPIO.IN)
GPIO.setup(relay_pins, GPIO.OUT)

a_subject = "State of the sensors at - {}" .format(dt_string)
a_message = ""

#reset all the relay ports, this should also switch off the light
for x in range(0,2):
    GPIO.output(relay_pins[x], GPIO.HIGH)

#this will switch on all the moisture sensors
print("Activation of relay at pin {}".format(relay_pins[0]))
# switches are triggered with LOW!!
GPIO.output(relay_pins[0], GPIO.LOW)
time.sleep(5) #wait for the sensor to sense something
do_send_mail = False

for pin in range(0,2): #only the one of the moist sensors
    a_message += "Test sequence for {}: ".format(pin)

    ms = GPIO.input(moist_pins[pin])
    a_message += "{}".format(ms)
    a_message +="\n"
    
    print("Using pin {0} for input - test returned {1}".format(moist_pins[pin], ms))

    if ms == 1:
        a_message += "{} need water\n" .format(pots[pin])
        do_send_mail = True
    else:
        a_message += "{} is wet enough\n" .format(pots[pin])

#turn off the sensors and avoid electrolisys        
GPIO.output(relay_pins[0], GPIO.HIGH)
time.sleep(1)

#now check the light sensor
light_level = rc_time(light_pin)
a_message += "\nLight level is: {}".format(light_level)
if light_level > LIGHT_TRESHOLD: # higher means darker
    if datetime.now().hour > 8 and datetime.now().hour < 18:
        ## only during the day
        GPIO.output(relay_pins[-1] , GPIO.LOW)
        a_message += "\nSwitching on the light"

print(a_subject)
print(a_message)
if do_send_mail: #not sending if only light and not water needed
    sendmail(a_subject, a_message)

#GPIO.cleanup() #this should also switch off the relays (switching off the lights)