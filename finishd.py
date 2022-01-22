from telegram import update
import RPi.GPIO as GPIO
from time import sleep
from telegram.ext import *
from threading import *
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  
import constants as keys
from picamera import PiCamera
import datetime
import cv2
import os

classNames = []
classFile = "/home/pi/Documents/farmdefence/coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

#This is to pull the information about what each object should look like
configPath = "/home/pi/Documents/farmdefence/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "/home/pi/Documents/farmdefence/frozen_inference_graph.pb"

#This is some set up values to get good results
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

animals = ['bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe']



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

GPIO.output(motor,1)

def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
#Below has been commented out, if you want to print each sighting of an object to the console you can uncomment below     
    #print(classIds,bbox)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in animals:
                
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                return className, img
            
    
    return False,img

def TelegramImg(t,name):
    print(t)
    for i in keys.CHAT_ID:

        updater.bot.sendPhoto(i,open(name,'rb'),caption = t)

def IrrigationMotor(): 
    print("irrigation started")
    GPIO.output(motor,0)
    sleep(3)
    GPIO.output(motor,1)
    print("irrigation Ended")    

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

def videoanalyzer():  
    cap = cv2.VideoCapture(0)
    print("camera called")
    cap.set(3,640)
    cap.set(4,480)
    #cap.set(10,70)
    #Below is the never ending loop that determines what will happen when an object is identified.    
    k = 0
    while k < 100:
        success, img = cap.read()
        print("image read")
#Below provides a huge amount of controll. the 0.45 number is the threshold number, the 0.2 number is the nms number)
        result,img = getObjects(img,0.45,0.2)
        k += 1
        if result:
            t = "{} animal detected".format(result)
            name = 'spot1.jpg'
            print(t)
            cv2.imwrite(name,img)
            print("image written")
            TelegramImg(t,name)
        #print(objectInfo)
            #cv2.imshow("Output",img)            
            #cv2.waitKey(5000)
            os.remove('spot1.jpg')
            print("imagedeleted")
            cap.release()
            break

def Motion_detect():   
    print("motion detection started")
    t = "intruder detected"
    videoanalyzer()
    Blinking_led_and_Buzzer(led)

updater = Updater(keys.API_KEY, use_context=True)
dp = updater.dispatcher
i = 0
while True:
    i += 1
    moisture = watermoniteringfunction()
    print(i)
    print(moisture)
    if not GPIO.input(fire):
        Fire_detection()
    elif GPIO.input(pir):
        Motion_detect()
    elif moisture < 30 and i%1000==0:
        TelegramBot("Automated Irrigation Started")
        IrrigationMotor()
        TelegramBot("Automated Irrigation Completed")
        i = 0
    else:
        Mainbotfunction()



      