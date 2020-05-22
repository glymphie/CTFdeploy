import time, datetime

t = list(time.strftime("%z"))

if t[0] == '+':
    utcdiff = (int(t[1]) * 36000 + (int(t[2]) - time.localtime().tm_isdst) * 3600 + int(t[3]) * 600 + int(t[4]) * 60)
    print('+' + str(utcdiff))
else:
    utcdiff = (int(t[1]) * 36000 + (int(t[2]) + time.localtime().tm_isdst) * 3600 + int(t[3]) * 600 + int(t[4]) * 60)
    print('-' + str(utcdiff))
