# -*- coding: utf-8 -*-
import time
import datetime

def string_to_datetime(s):
    if s:
        time_string = s.replace('T',' ')
        time_format = '%Y-%m-%d %H:%M:%S'
        mytime = time.strptime(time_string, time_format)
        return datetime.datetime(*mytime[:6])
    else:
        return s

def string_ymd_to_datetime(s):
    if s:
        time_format = '%Y-%m-%d'
        mytime = time.strptime(s, time_format)
        return datetime.datetime(*mytime[:6])
    else:
        return s

def string_dmy_to_date(s):
    try:
        d = s.split('/')
        return datetime.date(int(d[2]), int(d[1]), int(d[0]))
    except:
        return datetime.date.today()
