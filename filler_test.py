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




def filler():
    try:
        bucket = []
        t = 0
        forth = GPIO.input(18)
        
        if forth == False:    
                bucket.append(0)
                if len(bucket) == 9:
                    del bucket[-1]

        
        
        elif forth == True:
            
                bucket.append(1)
                if len(bucket) == 9:
                    del bucket[-1]
        
        
        
        if most_common(bucket) == 0:
            if t == 0:
                print ("Pool level A-OK")
                time.sleep(5)

            elif t == 1:
                t = 0
                print('Resetting GPIO')
                GPIO.cleanup()
                time.sleep(2)
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                
                """
                # Send email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                email = 'malachibazar@gmail.com'
                server.starttls()
                server.login(email, "Stuff180!")
                msg = 'Pool is full'
                server.sendmail(email, "8064704027@txt.att.net", msg) # 3038988643@vtext.com
                server.quit()
                """

            
        elif most_common(bucket) == 1:
            if t == 0:
                t = 1
                print('Flip\'n relay')
                GPIO.setup(17, GPIO.OUT)
                GPIO.output(17, 0)
                time.sleep(5)
                
                """
                # Send email
                server = smtplib.SMTP('smtp.gmail.com', 587)
                email = 'malachibazar@gmail.com'
                server.starttls()
                server.login(email, "Stuff180!")
                msg = 'Filling pool'
                server.sendmail(email, "8064704027@txt.att.net", msg) # 3038988643@vtext.com
                server.quit()
                """

            elif t == 1:
                print('Still fill\'n')
                time.sleep(5)
        print(bucket)
    except KeyboardInterrupt:
        GPIO.cleanup()

filler()