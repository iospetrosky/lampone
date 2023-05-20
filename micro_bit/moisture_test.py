from microbit import *
from random import randint
from time import sleep

def rc_time():
    count = 0
    #Output on the pin for 
    pin0.write_digital(0)
    sleep(0.1)
    while (pin0.read_digital() == 0):
        count += 1
    return count

def plot_light_level(light):
    if light > 5000:
        level = 5
    elif light > 2500:
        level = 4
    elif light > 1000:
        level = 3
    elif light > 500:
        level = 2
    elif light > 250:
        level = 1
    else:
        level = 0
    
    for i in range(0,5):
        display.set_pixel(4, i, 0)
    for i in reversed(range (0,level)):
        display.set_pixel(4, i, 5)
        
display.show ("X")

while True:
    plot_light_level(rc_time())
    sleep(5)
