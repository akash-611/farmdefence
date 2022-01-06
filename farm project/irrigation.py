import RPi.GPIO as GPIO
from time import sleep

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def IrrigationMotor(): 
    motor = 2
    GPIO.setup(motor,GPIO.OUT)
    GPIO.output(motor,1)
    sleep(30)
    GPIO.output(motor,0)

IrrigationMotor()
