from telegram.ext import *
import constants as keys
from threading import Thread
import RPi.GPIO as GPIO
from time import sleep

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

def IrrigationMotor(): 
    motor = 9
    GPIO.setup(motor,GPIO.OUT)
    GPIO.output(motor,1)
    sleep(30)
    GPIO.output(motor,0)

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
        IrrigationMotor()
        i = 1
    if i == 1:
        sleep(5)
        if GPIO.input(fire):
            t = "Fire Extinguished"
            TelegramBot(t)   

def Motion_detect():
    
    led = 18
    pir = 17
    GPIO.setup(pir,GPIO.IN)
    GPIO.setup(led,GPIO.OUT)
    i = GPIO.input(pir)
    t1 = Thread(target=Buzzer)
    t2 = Thread(target=Blinking_led,args=(led,))
    if i == 1:
        x = "intruder detected"
        print(x)
        t1.start()
        t2.start()
        TelegramBot(x)
            
        i = 0
        t1.join()
        t2.join()

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
        return "No water detected"

def TelegramBot(t):
    updater = Updater(keys.API_KEY,use_context=True)
    dp = updater.dispatcher
    j = updater.job_queue
    for i in keys.CHAT_ID:
        updater.bot.send_message(chat_id = i, text = t)

def start_command(update,context):
    update.message.reply_text('Hello! I am Jarvis, Your assistant\nAvailable Commands are:\n\t\t\t\t/watercontent')

def help_command(update,context):
    update.message.reply_text('wait right here!')

def water_content(update,context):
    response = Water_detection()
    update.message.reply_text(response)

def messagehandling(update, context):
    text = str(update.message.text).lower()
    if text:
        update.message.reply_text("available commands are: \n\t /watercontent")

def Messageresponse():
    print("waterdetection started")
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(CommandHandler("watercontent",water_content))
    dp.add_handler(MessageHandler(Filters.text, messagehandling))
    updater.start_polling()
    updater.idle()

i = Thread(target=Messageresponse)
j = Thread(target=Fire_detection)
k = Thread(target=Motion_detect)

i.start()
j.start()
k.start()
while True:
    i = 1
i.join()
j.join()
k.join()
