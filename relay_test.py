import time
import RPi.GPIO as GPIO

pin_list = [27]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_list, GPIO.OUT)




try:
    
    while True:
        h_r_l = raw_input('Enter high or low: ')

        if h_r_l == 'h' or h_r_l == 'high':
            GPIO.output(27, 1)
            print('high')
        elif h_r_l == 'l' or h_r_l == 'low':
            GPIO.output(27, 0)
            print('low')    
        
        
        
        
        
        
        


except KeyboardInterrupt:
    GPIO.cleanup()
