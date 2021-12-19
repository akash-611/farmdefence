from telegram import update
from telegram.ext import dispatcher, updater
import RPi.GPIO as GPIO
from time import sleep
from telegram.ext import *
import constants as keys

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def Blinking_led(i): #input "i" is bcm(gpio) pin number of led, declair gpio pin in function
    for j in range(0,3):
        GPIO.output(i,1)
        sleep(1)
        GPIO.output(i,0)

def Buzzer(i): #input "i" is 1 == high and 0 == low to turn on and off buzzer
    buzzer = 27
    GPIO.setup(buzzer,GPIO.OUT)
    GPIO.output(buzzer,i)

def Motion_detect():
    led = 18
    pir = 17
    GPIO.setup(pir,GPIO.IN)
    GPIO.setup(led,GPIO.OUT)
    while True:
        i = GPIO.input(pir)
        if i == 1:
            print("intruder detected")
            update.message.reply_text("intruder detected")
            Buzzer(1)
            Blinking_led(led)
            Buzzer(0)
            
        i = 0

def main():
    updater = Updater(keys.API_KEY,use_context=True)
    dp = updater.dispatcher
    Motion_detect()
    