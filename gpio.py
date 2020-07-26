import RPi.GPIO as GPIO
import time
motion_pin = 3

def main():
  while True:
    value=GPIO.input(motion_pin)  
    if value!=0:                             #to read the value of a GPIO pin
      time.sleep(2)        #delay 2ms
      print "on"                           #print information
    else:
      time.sleep(2)       #delay 2ms
      print "off"                         #print information
