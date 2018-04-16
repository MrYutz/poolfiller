#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from datetime import datetime
import smtplib
from collections import Counter
from datetime import datetime
import pandas as pd
import re


def most_common(lst):
    if lst != []:
        data = Counter(lst)
        return max(lst, key=data.get)


def add_time(str1, str2):
    pat1 = '(\d?\d):(\d\d):(\d\d)'
    reg1 = re.search(pat1, str1)
    reg2 = re.search(pat1, str2)
    
    if reg1 and reg2:
        seconds = int(reg1.group(3)) + int(reg2.group(3))
        minutes = int(reg1.group(2)) + int(reg2.group(2))
        hours = int(reg1.group(1)) + int(reg2.group(1))
        if seconds > 60:
            minutes_to_add = seconds // 60
            seconds_left_over = seconds % 60
            minutes = minutes + minutes_to_add
            seconds = seconds_left_over
        if minutes > 60:
            hours_to_add = minutes // 60
            minutes_left_over = minutes % 60
            hours = hours + hours_to_add
            minutes = minutes_left_over
        if seconds < 10:
            seconds = '0{}'.format(seconds)
        if minutes < 10: 
            minutes = '0{}'.format(minutes)

        total_time = '{}:{}:{}'.format(hours, minutes, seconds)
        return(total_time)



GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)


def filler(bucket, timer):
    now = datetime.now().strftime('%H:%M:%S')
    start_time = 0
    off_timer = False
    forth = GPIO.input(18)

    if most_common(bucket) == 0:
        if GPIO.input(17) == 1:
            GPIO.output(17, 0)
            off_timer = True
        else:
            pass
            
    elif most_common(bucket) == 1:
        if GPIO.input(17) == 0:
            GPIO.output(17, 1)
            start_time = now
        else:
            pass
            


    if forth == False:
        bucket.append(0)
        if len(bucket) == 10:
            del bucket[0]
        if off_timer == True:
            if timer == 1:
                return 0, timer, bucket, now
        else:
            return 0, timer, bucket, 0

    elif forth == True:
        bucket.append(1)
        if len(bucket) == 10:
            del bucket[0]
        if start_time != 0:
            if timer == 0:
                return 1, timer, bucket, start_time
        else:
            return 1, timer, bucket, 0
                

    
df = pd.read_csv('level.csv', index_col=False)
t = 0
bucket = []
FMT = '%H:%M:%S'
try:
    clock = 0
    while True:
        now = datetime.now()
        state, t, bucket, clock = filler(bucket, t)
        
        if t == 0 and clock != 0:
            start_time = clock
            t = 1
            print('Start Time: {}'.format(start_time))
        elif t == 1 and clock != 0:
            t = 0
            length_of_time = datetime.strptime(clock, FMT) - datetime.strptime(start_time, FMT)
            if len(df) > 0:
                if str(df.loc[len(df)-1][0]) == str(now.strftime('%m-%d-%y')):
                    df.loc[len(df)-1][1] = add_time(str(df.loc[len(df)-1][1]), str(length_of_time))
            else:
                df.loc[len(df)] = [str(now.strftime('%m-%d-%y')), str(length_of_time)]
            print('End Time: {}'.format(clock))
            print('Counter: {}'.format(t))
            print('State: {}'.format(state))
            print('Bucket: {}'.format(bucket))
            df.to_csv('level.csv', index=False)
            
        time.sleep(5)
except KeyboardInterrupt:
    print('\ncleaning GPIO')
    GPIO.output(17, 0)
    GPIO.cleanup()
    print('OK')

