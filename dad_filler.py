import RPi.GPIO as GPIO
import numpy as np
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)

pool_level = np.zeros(6)
print('Initial Pool Level:')
print(pool_level)

try:

    while True:
		
		print('Call for Water: %s' % GPIO.input(18))
		np.delete(pool_level,5)
				
		np.append(pool_level, GPIO.input(18))
			
		if np.average(pool_level) > 0.5 and GPIO.input(17) == 0:
			GPIO.output(17, 1)
			start_time = datetime.now()
			print('Start Time: {}'.format(start_time))
		elif  np.average(pool_level) < 0.5 and GPIO.input(17) == 1:
			GPIO.output(17, 0)
			np.zeros(pool_level)
			run_time = datetime.now() - start_time
			print('Run Time: {}'.format(run_time))
		else:
			GPIO.output(17, 0)
			str_pool_level = ','.join(str(p) for p in pool_level)
			print('Pool Level: %s' % str_pool_level)
			
		time.sleep(5)

			
except KeyboardInterrupt:
    print('\ncleaning GPIO')
    GPIO.output(17, 0)
    GPIO.cleanup()
    print('OK')