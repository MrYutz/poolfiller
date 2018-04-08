#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from datetime import datetime
import smtplib
from collections import Counter
from datetime import datetime

def most_common(lst):
    if lst != []:
        data = Counter(lst)
        return max(lst, key=data.get)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def filler(bucket, timer):
    now = datetime.now().strftime('%H:%M:%S')
    start_time = None
    forth = GPIO.input(18)

    if most_common(bucket) == 0:
        if timer == 0:
            pass
        elif timer == 2:
            t = 0
            GPIO.cleanup()
            time.sleep(.25)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    elif most_common(bucket) == 1:
        if timer == 0:
            
            GPIO.setup(17, GPIO.OUT)
            GPIO.output(17, 0)
            start_time = now
        elif timer == 1:
            pass
            


    if forth == False:
        bucket.append(0)
        if len(bucket) == 10:
            del bucket[0]
        if timer == 1:
            
            return 0, timer, bucket, now
        else:
            return 0, timer, bucket, None

    elif forth == True:
        bucket.append(1)
        if len(bucket) == 10:
            del bucket[0]
        if start_time != None:
            if timer == 0:
                
                return 1, timer, bucket, start_time
        else:
            return 1, timer, bucket, None
                

    

t = 0
bucket = []
try:
    timer = None
    while True:
        
        state, t, bucket, timer = filler(bucket, t)
        
        if t == 0 and timer != None:
            start_time = timer
            t = 1
            print('Start Time: {}'.format(start_time))
        elif t == 1 and timer != None:
            t = 2
            print('End Time: {}'.format(timer))
            print('Counter: {}'.format(t))
            print('State: {}'.format(state))
            print('Bucket: {}'.format(bucket))
            
        time.sleep(5)
except KeyboardInterrupt:
    print('\ncleaning GPIO')
    GPIO.cleanup()
    print('OK')

