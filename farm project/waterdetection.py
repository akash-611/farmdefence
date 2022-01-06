import RPi.GPIO as GPIO
from time import sleep
import spidev # To communicate with SPI devices
from numpy import interp  # To scale values
from time import sleep  # To add delay

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

spi = spidev.SpiDev() # Created an object
spi.open(0,0) 

# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

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

   
    output = analogInput(0) # Reading from CH0
    output = interp(output, [0, 1023], [100, 0])
    output = int(output)
    return "moisture = {}", output
   
