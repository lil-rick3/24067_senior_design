import RPi.GPIO as GPIO
from time import sleep

# Set up GPIO
led_pin = 17  # Change this to the GPIO pin you've connected the LED to
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

try:
    # Blink the LED 5 times
    for _ in range(5):
        print("LED ON")
        GPIO.output(led_pin, GPIO.HIGH)
        sleep(1)
        
        print("LED OFF")
        GPIO.output(led_pin, GPIO.LOW)
        sleep(1)

finally:
    # Clean up GPIO on program exit
    GPIO.cleanup()