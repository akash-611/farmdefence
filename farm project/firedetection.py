from telegram import update
from telegram.ext import dispatcher, updater
import RPi.GPIO as GPIO
from time import sleep
from telegram.ext import *
import constants as keys
import irrigation as extinguish

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def Blinking_led(i): #input "i" is bcm(gpio) pin number of led, declair gpio pin in function
    for j in range(0,3):
        GPIO.output(i,1)
        sleep(1)
        GPIO.output(i,0)
        sleep(1)


def TelegramBot(t):
    updater = Updater(keys.API_KEY,use_context=True)
    dp = updater.dispatcher
    j = updater.job_queue
    for i in keys.CHAT_ID:
        updater.bot.send_message(chat_id = i, text = t)
    

def Buzzer(): #input "i" is 1 == high and 0 == low to turn on and off buzzer
    buzzer = 27
    GPIO.setup(buzzer,GPIO.OUT)
    GPIO.output(buzzer,1)
    sleep(5)
    GPIO.output(buzzer,0)

def Fire_detection():
    fire = 24
    red = 25
    GPIO.setup(red,GPIO.OUT)

    GPIO.setup(fire,GPIO.IN)
    i = 0

    if not GPIO.input(fire):
        print("Fire Alert")
        Blinking_led(red)
        Buzzer()
        t = "Fire Alert"
        TelegramBot(t)
        extinguish.IrrigationMotor()
        i = 1
    if i == 1:
        sleep(5)
        if GPIO.input(fire):
            t = "Fire Extinguished"
            TelegramBot(t)   
def main():
    print("firedetection started")
    while True:
        Fire_detection()

main()