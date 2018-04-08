import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        first = GPIO.input(18)
        second = GPIO.input(23)
        third = GPIO.input(24)
        forth = GPIO.input(12)
        if first == False:
            print('Button 1 Pressed')
            time.sleep(5)
        elif second == False:
            print ("Button 2 Pressed")
            time.sleep(0.2)
        elif third == False:
            print("Button 3 Pressed")
            time.sleep(0.2)
        elif forth == False:
            print ("Button 4 Pressed")
            time.sleep(0.2)
        else:
            print('nothing happening')
            time.sleep(5)

except KeyboardInterrupt:
    GPIO.cleanup()