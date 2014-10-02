# use Python 3.3.3

import json
import urllib.request
import gzip
from datetime import datetime
import calendar
from collections import OrderedDict

def locationYear(usaf, wban, year):
    return(str(year)+'/'+str(usaf)+'-'+str(wban)+'-'+str(year)+'.gz')

def getTimeFromLine(line):
    yyyy, mm, dd = int(line[15:19]), int(line[19:21]), int(line[21:23]) # pos 16-23 YYYYMMDD
    h, m, s = int(line[23:25]), int(line[25:27]), 0 # pos 24 - 27 HHMM
    d = datetime(yyyy, mm, dd, h, m, s, 0)
    return(calendar.timegm(d.utctimetuple()))

data=[]
for i in range(2005, 2015):
    i = str(i)
    cincinnati = locationYear(724297, 93812, i)
    # Get the data
    with urllib.request.urlopen('ftp://ftp.ncdc.noaa.gov/pub/data/noaa//'+cincinnati) as file:
        # Open the gzip file (in bytes mode)
        with gzip.open(file, 'rb') as f:
                datapoints = []
                for line in f:
                    time = getTimeFromLine(line)
                    temp = float(line[87:92]) # pos 88-92 (offset by one due to Python 0 indexing)
                    if temp != 9999: # filter missing data
                        point = [time, temp]
                        datapoints.append(point)
                data = data + datapoints

p = OrderedDict([('id', 'myFirstTimeSeries'), ('description', 'prototype time series for discussion'), ('columns', ['time', 'value']), ('units', 'MGD'), ('mean', 0.75), ('stdDev', 2.3)])
d = OrderedDict([('type', 'series'), ('format', 'unixutc'), ('data', data), ('properties', p)])

with open('/Users/carolyn/temperatures_cincinnati.json', 'w') as outfile:
    json.dump(d, outfile, sort_keys=False, indent=2)
