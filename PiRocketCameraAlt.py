
import board
import adafruit_bmp3xx

from time import sleep
import RPi.GPIO as GPIO
from gpiozero import Button
from datetime import datetime

from picamera import PiCamera
from time import sleep

camera = PiCamera()

i2c = board.I2C()
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

bmp.sea_level_pressure =1021.64

bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

Button.was_held = False
btn = Button(17)

GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

GPIO.output(21, True)
GPIO.output(20, False)

print("Waiting.")
btn.wait_for_press()
    
GPIO.output(21, False)
GPIO.output(20, True)
print("Launch in 2 seconds.")

camera.start_preview()
camera.rotation = 0
camera.start_recording('/home/pi/Desktop/Trial1.h264')

sleep(2)

ButtonFree = True

while (ButtonFree):
    file = open("log.txt","a")
    file.write(datetime.today().strftime('%H:%M:%S'))
    file.write(' Alt: {:5.2f} m'.format(bmp.altitude))
    file.write("\n")
    file.close()
    print("Waiting for button press")
    sleep(0.1)
    if btn.is_pressed:
        ButtonFree = False   

camera.stop_recording()
camera.stop_preview()
print("I'm done!")
GPIO.cleanup()

#i2c = board.I2C()
#bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)

#bmp.sea_level_pressure =1021.64

#bmp.pressure_oversampling = 8
#bmp.temperature_oversampling = 2

#print("Pressure: {:6.2f} Temperature: {:5.2f}".format(bmp.pressure, bmp.temperature))
#print('Altitude: {:5.2f} meters'.format(bmp.altitude))
