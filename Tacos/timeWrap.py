'''
This Tacos is responsible for all time-related wrap(pers)
'''

import pytz
from datetime import datetime

def nowInZone(zone:str= 'Asia/Singapore'):
  local_tz = pytz.timezone(zone)
  now = datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz)
  return now
