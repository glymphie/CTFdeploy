"""
Calculates the local time difference and accounts for daylight saving
"""
import time

t = time.strftime("%z")

if t[0] == '+':
    utcdiff = ((int(t[1:3]) - time.localtime().tm_isdst) * 3600 + int(t[3:5]) * 60)
    print('+' + str(utcdiff))
else:
    utcdiff = ((int(t[1:3]) + time.localtime().tm_isdst) * 3600 + int(t[3:5]) * 60)
    print('-' + str(utcdiff))
