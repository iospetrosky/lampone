#!/usr/bin/env python3
import RPi.GPIO as GPIO
import smbus
import time
import smtplib # This is the SMTP library we need to send the email notification
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

class Moisture:
    def __init__(self, channel, pot):
        self.Channel = channel
        self.Pot = pot
        self.MoistRead = 0

address = 0x48 # test with command: i2cdetect -y 1

moistures = [
    Moisture(0x40, 'Strawberry'),
    Moisture(0x41, 'Forest')
]

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
        return "DRY!!"
    if value > 150:
        return "Need water"
    if value > 100:
        return "Barely enough"
    if value > 50:
        return "Wet enough"
    ## else
    return "Too wet!!"


### MAIN ###
relay_off()
time.sleep(2) # give a moment for the configuration to take effect
relay_on()
time.sleep(2) # wait for some measurements are actually made
for moist in moistures:
    print("Checking pot {} channel {}".format(moist.Pot,moist.Channel))
    moisture = 0
    
    for i in range(1,10):
        bus.write_byte(address,moist.Channel) # Activate analog channel
        moisture = bus.read_byte(address)
        print("Moisture detected: {}".format(moisture))

    print("Last reading: {}".format(moisture))
    moist.MoistRead = moisture

relay_off()
destroy()

a_subject = "Moisture reading at {}".format(dt_string)
a_message = ""

for moist in moistures:
    a_message = "{}\nReading for {} is: {} - {}".format(a_message,moist.Pot, moist.MoistRead, comment(moist.MoistRead))

print(a_subject)
print(a_message)

sendmail(a_subject, a_message)
