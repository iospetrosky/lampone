#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import smtplib # This is the SMTP library we need to send the email notification
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


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

moist_pin = 8
relay_pins = [7,11]

# returns 0 when the moisture led is on meaning that the soil
# is moist enough - when it turns to 1 it means watering is needed
GPIO.setmode(GPIO.BOARD) # phisical bnoard

GPIO.setup(moist_pin, GPIO.IN)
GPIO.setup(relay_pins, GPIO.OUT)

GPIO.output(relay_pins[1], GPIO.HIGH)
GPIO.output(relay_pins[0], GPIO.HIGH)

print("Activation of relay at pin {}".format(relay_pins[0]))
# switches are triggered with LOW!!
GPIO.output(relay_pins[0], GPIO.LOW)

time.sleep(5) #wait for the sensor to sense something

a_message = "Test sequence: "
for x in range(1,75):
    ms = GPIO.input(moist_pin)
    a_message = "{}{}".format(a_message, ms)
    time.sleep(0.1)

#ms = GPIO.input(moist_pin)
print("Using pin {0} for input - test returned {1}".format(moist_pin, ms))

if ms == 1:
    a_subject = "Le fragole devono essere innaffiate - {}" .format(dt_string)
else:
    a_subject = "Le fragole stanno bene - {}".format(dt_string)

#GPIO.output(relay_pins[0], GPIO.HIGH)
GPIO.cleanup() #this should also switch off the relay

print(a_subject)
print(a_message)

#sendmail(a_subject, a_message)
