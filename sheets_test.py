from datetime import datetime
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

gc = gspread.authorize(credentials)

# Open the Log Sheet
sheet = gc.open_by_key('1-KODd3dNss0_NaZbbHfN-i4DvidqPToa4mCBpyemHLM').sheet1

print ('Row Count: %s' % sheet.row_count)


values = ['', '', '', str(datetime.now())]
sheet.append_row(values)

start_time = datetime.now()
sheet = gc.open_by_key('1-KODd3dNss0_NaZbbHfN-i4DvidqPToa4mCBpyemHLM').sheet1
print ('Row Count: %s' % sheet.row_count)
values = [str(start_time), 'Running', 'Running']
sheet.append_row(values)

time.sleep (2)

end_time = datetime.now()

run_time = end_time - start_time

row = [str(start_time), str(end_time), run_time.total_seconds()]

sheet = gc.open_by_key('1-KODd3dNss0_NaZbbHfN-i4DvidqPToa4mCBpyemHLM').sheet1
print ('Row Count: %s' % sheet.row_count)
index = sheet.row_count
sheet.delete_row(index)
sheet.append_row(row)
