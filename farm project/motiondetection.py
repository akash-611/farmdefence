import RPi.GPIO as GPIO
from time import sleep
from telegram.ext import *
import constants as keys
from threading import Thread

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def Blinking_led(i): #input "i" is bcm(gpio) pin number of led, declair gpio pin in function
    for j in range(0,3):
        GPIO.output(i,1)
        sleep(1)
        GPIO.output(i,0)
        sleep(1)

def Buzzer(): #input "i" is 1 == high and 0 == low to turn on and off buzzer
    buzzer = 27
    GPIO.setup(buzzer,GPIO.OUT)
    for i in range(5):
        GPIO.output(buzzer,1)
        sleep(1)
        GPIO.output(buzzer,0)
        sleep(0.3)

def Motion_detect():
    
    led = 18
    pir = 17
    GPIO.setup(pir,GPIO.IN)
    GPIO.setup(led,GPIO.OUT)
    i = GPIO.input(pir)
    t1 = Thread(target=Buzzer)
    t2 = Thread(target=Blinking_led,args=(led,))
    if i == 1:
        print("intruder detected")
        t1.start()
        t2.start()
        TelegramBot()
            
        i = 0
        t1.join()
        t2.join()

def TelegramBot():
    updater = Updater(keys.API_KEY,use_context=True)
    dp = updater.dispatcher
    j = updater.job_queue
    for i in keys.CHAT_ID:
        updater.bot.send_message(chat_id = i, text ="intruder detected")
    


def main():
    
    print("main function running")
    updater = Updater(keys.API_KEY,use_context=True)
    dp = updater.dispatcher
    j = updater.job_queue
    
    while (True):
        Motion_detect() #CHANGES DONE HERE

main()
