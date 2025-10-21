import RPi.GPIO as GPIO
import time

MotorPin1   = 19
MotorPin2   = 26
MotorEnable = 5
PWM_FREQUENCY = 1000  # Hz

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MotorPin1, GPIO.OUT)
    GPIO.setup(MotorPin2, GPIO.OUT)
    GPIO.setup(MotorEnable, GPIO.OUT)

    global pwm
    pwm = GPIO.PWM(MotorEnable, PWM_FREQUENCY)
    pwm.start(0)  # Start with motor stopped

def set_motor(direction, speed_percent):
    """
    direction: 'clockwise' or 'anticlockwise'
    speed_percent: 0 to 100
    """
    pwm.ChangeDutyCycle(speed_percent)
    if direction == 'clockwise':
        GPIO.output(MotorPin1, GPIO.HIGH)
        GPIO.output(MotorPin2, GPIO.LOW)
    elif direction == 'anticlockwise':
        GPIO.output(MotorPin1, GPIO.LOW)
        GPIO.output(MotorPin2, GPIO.HIGH)

def stop_motor():
    pwm.ChangeDutyCycle(0)


def loop():
    while True:
        for speed in [20,30,40,50,60,70,80,90,100]:
            print(f"Speed is {speed}")
            set_motor('anticlockwise',speed)
            time.sleep(5)
        print("Stopped")
        stop_motor()
        time.sleep(5)

def old_loop():
    while True:

        print("Press Ctrl+C to end the program...")

        print("Spin clockwise at 40% speed")
        set_motor('clockwise', 20)
        time.sleep(5)

        # stop_motor()
        # time.sleep(2)

        print("Spin clockwise at 80% speed")
        set_motor('clockwise', 80)
        time.sleep(5)

        stop_motor()
        time.sleep(2)

        print("Spin anticlockwise at 50% speed")
        set_motor('anticlockwise', 50)
        time.sleep(5)

        print("Spin anticlockwise at 100% speed")
        set_motor('anticlockwise', 100)
        time.sleep(5)

        stop_motor()
        time.sleep(2)

def destroy():
    stop_motor()
    pwm.stop()
    GPIO.cleanup()

def sample():
    print("initial spin")
    set_motor('anticlockwise', 100)
    time.sleep(0.1)
    print("lowest speed")
    set_motor('anticlockwise', 40)
    time.sleep(5)


if __name__ == '__main__':
    setup()
    sample()
    destroy()

    # try:
    #     loop()
    # except KeyboardInterrupt:
    #     destroy()