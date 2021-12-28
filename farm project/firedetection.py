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


def TelegramBot():
    
    updater.bot.send_message(chat_id = keys.CHAT_ID, text ="fire alert")
    

def Buzzer(i): #input "i" is 1 == high and 0 == low to turn on and off buzzer
    buzzer = 27
    GPIO.setup(buzzer,GPIO.OUT)
    GPIO.output(buzzer,i)

def Fire_detection():
    fire = 24
    red = 25
    GPIO.setup(red,GPIO.OUT)

    GPIO.setup(fire,GPIO.IN)

   
    if not GPIO.input(fire):
        print("Fire Alert")
        Blinking_led(red)
        Buzzer(1)
        TelegramBot()
        extinguish.IrrigationMotor()
        Buzzer(0)
      
if __name__ == "__main__":
    updater = Updater(keys.API_KEY,use_context=True)
    dp = updater.dispatcher
    j = updater.job_queue
    while True:
        Fire_detection()