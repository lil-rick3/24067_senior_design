import time
import os 
import subprocess 
from gpiozero import Button

button = Button(17)
turnOff = False

while True: 
    if button.is_pressed:
        if turnOff: 
            time.sleep(1)
            if button.is_pressed:
                os.system("kill $(pgrep -f 'python main.py')")
                time.sleep(1)
                os.system("shutdown -h now")
        else: 
            turnOff = True 
            time.sleep(1)
            if button.is_pressed: 
                print("\nRunning sorting script...\n")
                fileName = r"/home/jaret/Scripts/main.py"
                cmd = ['python3', fileName]
                subprocess.run(cmd)
    time.sleep(1)

