from adafruit_servokit import ServoKit
import time
import board
import busio
import serial
import RPi.GPIO as GPIO
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

#------------------------------------ Setup -------------------------------------

# Initialize I2C bus 
i2c = board.I2C() 

# Initialise the LCD class
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, 16, 2)

#setup for serial input/output
ser = serial.Serial("/dev/ttyUSB0", 9600)  
ser.baudrate = 9600

#set pin modes for relay drivers
vibMotor = 27
vexMotor = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(vibMotor, GPIO.OUT)
GPIO.setup(vexMotor, GPIO.OUT)

#sorting mode elements 
modes = ['Color', 'Shape', 'Size', 'Character']
currentMode = None
sortingIndex = 0 

#classification elements 
classified = False 
category = 0
colors = []
shapes = []
sizes = []
characters = []

#servo angles that correspond to each bin
binAngles = [7.5, 22.5, 37.5, 52.5, 67.5, 82.5, 97.5, 112.5, 127.5, 142.5, 157.5, 172.5]

#initialize servos 
kit = ServoKit(channels = 16)
kit.servo[0].set_pulse_width_range(500, 2500)
kit.servo[2].set_pulse_width_range(500, 2500)

#set servo angle ranges
kit.servo[0].actuation_range = 180
kit.servo[2].actuation_range = 180
kit.servo[0].angle = 0
kit.servo[2].angle = 0

#------------------------------------- LCD ---------------------------------------

lcd.clear()
lcd.message = "Choose mode:\n" + modes[sortingIndex].ljust(9)

while True: 
    if lcd.left_button:
        if sortingIndex != 0: 
            sortingIndex = sortingIndex - 1
        else: 
            sortingIndex = 3
        lcd.message = "Choose mode:\n" + modes[sortingIndex].ljust(9)
    elif lcd.right_button:
        if sortingIndex != 3: 
            sortingIndex = sortingIndex + 1
        else: 
            sortingIndex = 0
        lcd.message = "Choose mode:\n" + modes[sortingIndex].ljust(9)
    elif lcd.select_button:
        lcd.message = "Mode selected:\n" + modes[sortingIndex].ljust(9)
        currentMode = modes[sortingIndex]
        break 

#------------------------------------ Control Sequence -------------------------------------

#send data to Arudino for lights and break beam
ser.write(b'1\n')

##################################
#choose computer vision model 
##################################

#turn on conveyor belt 
GPIO.output(vexMotor, GPIO.HIGH)
#turn on vibrational motor
GPIO.output(vibMotor, GPIO.HIGH)

while(1):
    #wait for break beam to go low
    if ser.read() == b'1':
        #turn vibrational motor off
        GPIO.output(vibMotor, GPIO.LOW)

        ###########################
        #IMAGE CLASSIFICATION
        ###########################

        #----------sorting arm servo-----------------
        kit.servo[2].angle = binAngles[category]
        time.sleep(0.2)
        #----------trap-door servo-------------------
        #if bead has been classified, open trap door 
        kit.servo[0].angle = 90
        time.sleep(0.5)
        #move trap door servo back to starting position
        kit.servo[0].angle = 0
        #turn vibrational motor back on
        GPIO.output(vibMotor, GPIO.HIGH)

        if category < 12: 
            category = category + 1
        else: 
            break 