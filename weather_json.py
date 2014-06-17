import json
import urllib.request
import gzip
from datetime import datetime
import calendar

def locationYear(usaf, wban, year):
    return(str(year)+'/'+str(usaf)+'-'+str(wban)+'-'+str(year)+'.gz')

def getTimeFromLine(line):
    yyyy, mm, dd = int(line[15:19]), int(line[19:21]), int(line[21:23])
    h, m, s = int(line[23:25]), int(line[25:27]), 0
    d = datetime(yyyy, mm, dd, h, m, s, 0)
    return(calendar.timegm(d.utctimetuple()))

for i in range(1989, 2014):

    i = str(i)
    cincinnati = locationYear(724297, 93812, i)

    # Acquire the data
    with urllib.request.urlopen('ftp://ftp.ncdc.noaa.gov/pub/data/noaa//'+cincinnati) as file:
    
        # Open the gzip file (in bytes mode)
        with gzip.open(file, 'rb') as f:
            
            with open('/Users/carolyn/Documents/D3js/json project/cincyWeather'+ i +'.json', 'w') as outfile:

                for line in f:
                    time = getTimeFromLine(line)
                    temp = float(line[87:92])
                    objects_list=[]
                    for i in enumerate(f):
                        if temp != 9999:        # Filter out the missing data
                            d = dict([('time', time), ('value', temp)])
                            objects_list.append(d)
                        else:
                            continue
                    json.dump(objects_list, outfile)
