from telegram import update
import RPi.GPIO as GPIO
from time import sleep
from telegram.ext import *
from threading import *
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  
import constants as keys


GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

spi = spidev.SpiDev() # Created an object
spi.open(0,0) 

motor = 5
buzzer = 27
led = 18
pir = 17
fire = 24
red = 25
GPIO.setup(red,GPIO.OUT)
GPIO.setup(motor,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(fire,GPIO.IN)
GPIO.setup(pir,GPIO.IN)
GPIO.setup(led,GPIO.OUT)


def IrrigationMotor(): 
    print("irrigation started")
    GPIO.output(motor,1)
    sleep(3)
    GPIO.output(motor,0)

def Blinking_led_and_Buzzer(i): #input "i" is bcm(gpio) pin number of led, declair gpio pin in function
    print("led blinking begins")
    for _ in range(0,3):
        GPIO.output(i,1)
        GPIO.output(buzzer,1)
        sleep(1)
        GPIO.output(i,0)
        GPIO.output(buzzer,0)
        sleep(1)

def TelegramBot(t):
    print(t)
    for i in keys.CHAT_ID:
        updater.bot.send_message(chat_id = i, text = t)

def analogInput(channel):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def start_command(update,context):
    update.message.reply_text('Hello! I am Jarvis, Your assistant\nAvailable Commands are:\n\t\t\t\t/watercontent')

def help_command(update,context):
    update.message.reply_text('wait right here!')

def water_content(update,context):
    response ="the moisture content is : " + str(watermoniteringfunction())
    update.message.reply_text(response)

def messagehandling(update, context):
    text = str(update.message.text).lower()
    if text:
        update.message.reply_text("available commands are: \n\t /watercontent \n\t /irrigation")

def Manualirrigation(update, context):
    update.message.reply_text("irrigation begins")
    IrrigationMotor()
    update.message.reply_text("irrigation ends")

def Mainbotfunction():
    print("main bot function started")
    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(CommandHandler("help",help_command))
    dp.add_handler(CommandHandler("watercontent",water_content))
    dp.add_handler(CommandHandler("irrigation",Manualirrigation))
    dp.add_handler(MessageHandler(Filters.text, messagehandling))
    updater.start_polling()
    #updater.stop()

def watermoniteringfunction():
    print("water monitering funciton started")
    output = analogInput(0) # Reading from CH0
    output = interp(output, [0, 1023], [100, 0])
    output = int(output)
    return output


def Fire_detection():

    i = 0
    print("fire detection started")
    print("Fire Alert")
    Blinking_led_and_Buzzer(red)
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
    
    print("motion detection started")
    t = "intruder detected"
    TelegramBot(t)
    Blinking_led_and_Buzzer(led)

updater = Updater(keys.API_KEY, use_context=True)
dp = updater.dispatcher

while True:
    moisture = watermoniteringfunction()
    print(moisture)
    if not GPIO.input(fire):
        Fire_detection()
    elif GPIO.input(pir):
        Motion_detect()
    elif moisture < 30:
         IrrigationMotor()
         TelegramBot("irrigation started")
    else:
        Mainbotfunction()


      