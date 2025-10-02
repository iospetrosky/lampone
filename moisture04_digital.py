#!/usr/bin/env python3
import RPi.GPIO as GPIO
import smbus # remember to activate I2C with 'sudo raspi-config'
import time
import smtplib # This is the SMTP library we need to send the email notification
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import mysql.connector as mysql
import requests

class Moisture:
    def __init__(self, channel, pot, tsp_field): ## last param is the field in thingspeak
        self.Channel = channel
        self.Pot = pot
        self.MoistRead = 0
        self.ThingSpeskField = tsp_field

address = 0x48 # test with command: i2cdetect -y 1

# 0x40 = red/gray wires
# 0x41 = blue/green wires

moistures = [
    Moisture(0x40, 'Peperoncini', "field2"),
    Moisture(0x41, 'Rose', "field3")
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
    if value > 170:
        return "Need water"
    if value > 120:
        return "Barely enough"
    if value > 60:
        return "Wet enough"
    ## else
    return "Too wet!!"


### MAIN ###
mydb = mysql.connect(
    host="localhost",
    user="pi",
    password="emberlee1",
    database='iam'
    #use_pure=True
)
cur = mydb.cursor(dictionary=True)

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
    cur.execute("insert into sensor_measures (pot, measure) values ('{}',{})".format(moist.Pot, moist.MoistRead))
    # now also save the data on thingspeak
    url = "https://api.thingspeak.com/update?api_key=DSS1C6ZEID5ZBE2S&{}={}".format(moist.ThingSpeskField, moist.MoistRead)
    print(url)
    requests.get(url)
    time.sleep(35) ## ThingSpeak is not happy if the requests are too fast

mydb.close()

a_message = "{}\n - Check stats here\nhttps://thingspeak.mathworks.com/channels/2731177".format(a_message)

print(a_subject)
print(a_message)

sendmail(a_subject, a_message)
