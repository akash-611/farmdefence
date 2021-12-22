import RPi.GPIO as GPIO
from time import sleep
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def Blinking_led(i): #input "i" is bcm(gpio) pin number of led, declair gpio pin in function
    for _ in range(0,3):
        GPIO.output(i,1)
        sleep(1)
        GPIO.output(i,0)

def Water_detection():
    moisture = 22
    red = 23
    GPIO.setup(red,GPIO.OUT)

    GPIO.setup(moisture,GPIO.IN)

   
    if not GPIO.input(moisture):
        print("water detected")
        Blinking_led(red)
        return "water detected"
    else:
        return "No water detec"
        
    
