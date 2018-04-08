#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from datetime import datetime
import smtplib
from collections import Counter

def most_common(lst):
    data = Counter(lst)
    return max(lst, key=data.get)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def filler(bucket, timer):
    
        
    forth = GPIO.input(18)

    if most_common(bucket) == 0:
        if timer == 0:
            pass
        elif timer == 1:
            timer = 0
            GPIO.cleanup()
            time.sleep(.25)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    elif most_common(bucket) == 1:
        if timer == 0:
            timer = 1
            GPIO.setup(17, GPIO.OUT)
            GPIO.output(17, 0)
        elif timer == 1:
            pass
            


    if forth == False:
        bucket.append(0)
        if len(bucket) == 10:
            del bucket[0]    
        return 0, timer, bucket

    elif forth == True:
        bucket.append(1)
        if len(bucket) == 10:
            del bucket[0]
        return 1, timer, bucket
                

    

t = 0
bucket = [0]
try:
    while True:
        state, t, bucket = filler(bucket, t)
        print('State: {}'.format(state))
        print('t: {}'.format(t))
        print('Bucket: {}'.format(bucket))
        time.sleep(2)
except KeyboardInterrupt:
    print('\ncleaning GPIO')
    GPIO.cleanup()
    print('OK')

