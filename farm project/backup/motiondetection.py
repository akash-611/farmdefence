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
    print("motion function started")
    led = 18
    pir = 17
    GPIO.setup(pir,GPIO.IN)
    GPIO.setup(led,GPIO.OUT)
    i = GPIO.input(pir)
    if i == 1:
        print("intruder detected")
        Buzzer(1)
        Blinking_led(led)
        TelegramBot()
        Buzzer(0)
            
        i = 0

def TelegramBot():
    updater = Updater(keys.API_KEY,use_context=True)
    dp = updater.dispatcher
    j = updater.
    for i in keys.CHAT_ID:
        updater.bot.send_message(chat_id = i,.CHAT_ID, text ="intruder detected")
    


def main():
    
    print("main function running")
    updater = Updater(keys.API_KEY,use_context=True)
    dp = updater.dispatcher
    j = updater.job_queue
    
    while (True):
        Motion_detect() #CHANGES DONE HERE

main()