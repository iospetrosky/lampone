#!/usr/bin/env python3
import RPi.GPIO as GPIO
import smbus
import time
import smtplib # This is the SMTP library we need to send the email notification
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

address = 0x48 # test with command: i2cdetect -y 1
Analogs = [0x40, 0x41] # list of active analog inputs
Relay = 7 # pin to control the relay

GPIO.setmode(GPIO.BOARD) # phisical board
GPIO.setup(Relay, GPIO.OUT)

bus = smbus.SMBus(1)
dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def destroy():
    print("Destroy")
    GPIO.output(Relay,GPIO.HIGH)    
    GPIO.cleanup()     

def relay_on():
    print("Relay on")
    GPIO.output(Relay,GPIO.HIGH)

def relay_off():
    print("Relay off")
    GPIO.output(Relay,GPIO.LOW)

## send the notification via email
def sendmail(subject, text_message):
    smtp_username = "loruk371@gmail.com" 
    smtp_password = "tiudnygltapfymks" 

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

def comment(value):
    if value > 200:
        return "Pretty wet"
    if value > 150:
        return "Wet enough"
    if value > 100:
        return "Barely enough"
    if value > 50:
        return "Need water"
    ## else
    return "DRY!!"


### MAIN ###
relay_off()
time.sleep(2) # give a moment for the configuration to take effect
relay_on()
time.sleep(2) # wait for some measurements are actually made
bus.write_byte(address,Analogs[0])
moisture = 0
for i in range(1,5):
    moisture = bus.read_byte(address)
    print("Moisture detected: {}".format(moisture))

print("Last reading: {}".format(moisture))

relay_off()
destroy()

a_subject = "Moisture reading at {}".format(dt_string)
a_message = "Reading is: {} - {}".format(moisture, comment(moisture))

print(a_subject)
print(a_message)

#sendmail(a_subject, a_message)
