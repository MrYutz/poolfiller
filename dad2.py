import RPi.GPIO as GPIO
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Setup Link to Google Sheets

scope = ['https://spreadsheets.google.com/feeds',
		 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('../.credentials/client_secret.json', scope)
gc = gspread.authorize(credentials)

# Open the Log Sheet
sheet_key = '1ZlrNKgob4UIh2wqLGrsJI6ZrXUVqFOcrR1Wp0mEMMSA'
sheet = gc.open_by_key(sheet_key).sheet1

# Setup GPIO on Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)

pool_level = [0] * 5
bol_filling = 0
min_run_time = 120

# Log the Launch of the Program / Startup Time
values = ['', '', '', str(datetime.now())]
sheet.append_row(values)

try:

	while True:
		# Trim the array to only have 5 items in it.  We don't want it to get long / have over 30 seconds of data.
		del pool_level[4:]

		#Read the pool level and add to front of array.
		pool_level.insert(0, GPIO.input(18))

		# Get average pool level using a float on the numerator.
		avg_pool_level = float(sum(pool_level)) / len(pool_level)

		print('START ---- Call for Water: %s, Avg: %s' % (GPIO.input(18), avg_pool_level))

		# check to see if we need to fill and this is the first time we have called for water.
		# run for a minimum of min_run_time seconds.
		if avg_pool_level > 0.5 and bol_filling == 0:
			GPIO.output(17, 1)
			start_time = datetime.now()
			print('Start Time: {}'.format(start_time))

			# log the start of the fill cycle....if the Pi dies at least we will have a start time.
			values = [str(start_time), 'Running', 'Running']

			# Reopen the sheet for writing and update rows etc.
			sheet = gc.open_by_key(sheet_key).sheet1
			sheet.append_row(values)

			# set filling latching variable to TRUE so we can later test and keep filling.
			bol_filling = 1
			# Latch ON and fill for a minimum of 120 seconds.  This prevents frequent on / off cycles.
			time.sleep(min_run_time)

		# We have a condition where we need to continue to run
		elif avg_pool_level > 0.5 and bol_filling == 1:
			# Wait 5 seconds before taking another reading and starting the process over.
			time.sleep(5)

		# The call for water has passed.  We need to log run time and clean up / shut off water.
		elif  avg_pool_level < 0.5 and GPIO.input(17) == 1:
			# Turn off the water
			GPIO.output(17, 0)
			# Zero out the fill array as an additional form of debounce.
			pool_level = [0] * 5
			bol_filling = 0
			end_time = datetime.now()
			run_time = end_time - start_time
			print('End Time: {}'.format(end_time))
			print('Run Time: {}'.format(run_time))

			# Reopen the sheet for writing and update rows etc.
			sheet = gc.open_by_key(sheet_key).sheet1
			row = [str(start_time), str(end_time), run_time.total_seconds()]
			index = sheet.row_count
			sheet.delete_row(index)
			sheet.append_row(row)


		# We are just waiting for a call for water.  Turn off the valves just in case; each loop.
		else:
			GPIO.output(17, 0)
			bol_filling = 0
			#print('ELSE ----- Call for Water: %s, Avg: %s' % (GPIO.input(18), avg_pool_level))
			# Wait 5 seconds before taking another reading and starting the process over.
			time.sleep(5)

except KeyboardInterrupt:
	print('\ncleaning GPIO')
	GPIO.output(17, 0)
	GPIO.cleanup()
	print('OK')

else:
	print('\ncleaning GPIO')
	GPIO.output(17, 0)
	GPIO.cleanup()
	print('OK')
