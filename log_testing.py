import pandas as pd
from datetime import datetime
from time import sleep
import re

df = pd.read_csv('level.csv', index_col=False)

FMT = '%H:%M:%S'
t = 0


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

    else:
        print('failed reg')


for i in range(5):
    if t == 0:
        t = 1
        now = datetime.now()
        time = now.strftime('%H:%M:%S')
        #print(time)
        sleep(3)
    elif t == 1:
        t = 0
        length_of_time = datetime.strptime(datetime.now().strftime('%H:%M:%S'), FMT) - datetime.strptime(time, FMT)
        if str(df.loc[len(df)-1][0]) == str(now.strftime('%m-%d')):
            
            df.loc[len(df)-1][1] = add_time(str(df.loc[len(df)-1][1]), str(length_of_time))
        else:
            df.loc[len(df)] = [str(now.strftime('%m-%d')), str(length_of_time)]
        sleep(1)

df.to_csv('level.csv', index=False)