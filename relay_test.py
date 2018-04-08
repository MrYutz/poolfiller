import time
import RPi.GPIO as GPIO

pin_list = [17, 27]

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_list, GPIO.OUT)




try:
    
    while True:
        
        GPIO.output(17, 1)
        GPIO.output(27, 1)
        print('high')
        time.sleep(3)
        
        GPIO.output(17, 0)
        GPIO.output(27, 0)
        print('low')
        time.sleep(3)


except KeyboardInterrupt:
    GPIO.cleanup()
