# use Python 3.3.3

import sqlite3
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

def parseWeatherData():
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
                            point = [time, temp/10] # noaa temp is scaled by a factor of 10
                            datapoints.append(point)
                    data = data + datapoints
    return data
    # data is a list of [time, value] pairs of length 113,893 for range(2005, 2015)

data = parseWeatherData()

def createTempoJSON(data): 
    p = OrderedDict([('id', 'myFirstTimeSeries'), ('description', 'prototype time series for discussion'), ('columns', ['time', 'value']), ('units', 'MGD'), ('mean', 0.75), ('stdDev', 2.3)])
    d = OrderedDict([('type', 'series'), ('format', 'unixutc'), ('data', data), ('properties', p)])
    with open('/Users/carolyn/temperatures_cincinnati.json', 'w') as outfile:
        json.dump(d, outfile, sort_keys=False, indent=2)

def temperatureTable(data):
    conn = sqlite3.connect("weather.db")
    c = conn.cursor()

    # meta table
    c.execute('''CREATE TABLE IF NOT EXISTS 'meta' ('series_id' INTEGER PRIMARY KEY ASC AUTOINCREMENT, 'name' TEXT UNIQUE ON CONFLICT ABORT, 'units' TEXT, 'regular_period' INTEGER, 'regular_offset' INTEGER)''')

    row = [['temperature', 'degrees Celsius']]
    c.executemany('''INSERT OR IGNORE INTO meta (name, units) VALUES (?, ?)''', (row))
    
    # points table
    c.execute('''CREATE TABLE IF NOT EXISTS 'temp' ('time' INTEGER, 'series_id' INTEGER REFERENCES 'meta'('series_id'), 'value' REAL, 'confidence' REAL, 'quality' INTEGER)''')
    for i in data:
        i = i+[1]+[0]+[0]
        c.execute('''INSERT OR IGNORE INTO temp (time, value, series_id, quality, confidence) VALUES (?, ?, ?, ?,?)''', (i))

    conn.commit()
    conn.close()

temperatureTable(data)
