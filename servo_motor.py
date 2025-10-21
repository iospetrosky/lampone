import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to the servo signal wire
servo_pin = 21

# Set up the pin as output
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM instance with 50Hz frequency (standard for servos)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)  # Start with 0% duty cycle

def set_angle(angle):
    """Set servo angle (0 to 180 degrees)."""
    duty = 2 + (angle / 18)  # Map angle to duty cycle
    print(duty)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)  # Allow time to move
    pwm.ChangeDutyCycle(0)  # Stop sending signal to avoid jitter

def cycle3():
    for angle in [0, 45, 110, 180]:
        print(f"Moving to {angle}°")
        set_angle(angle)
        time.sleep(5)


try:
    while True:
        cycle3()
except KeyboardInterrupt:
    print("Stopping...")

finally:
    set_angle(0)
    pwm.stop()
    GPIO.cleanup()