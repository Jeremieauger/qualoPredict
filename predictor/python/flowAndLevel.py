# -*- coding: utf-8 -*-
import os, re, requests, datetime
from sqlalchemy import create_engine
from lxml import html
from connector import *

# Removing the characters that mess with python
def strip_non_ascii(string):
    ''' Returns the string with ascii characters'''
    stripped = (c for c in string if 0 <= ord(c) <= 127)
    return ''.join(stripped)

# Accessing the data from the gouv. datamart
r = requests.get('http://dd.weather.gc.ca/hydrometric/csv/QC/hourly/QC_02OA016_hourly_hydrometric.csv')
data = strip_non_ascii(r.text)
rows = data.split("\r\n")
colNames = rows.pop(0) #removing colnames row

# Selecting the most recent predictions for the level and flow
levels = {}
flows = {}
for row in rows:
    if len(row) < 2:
        continue
    row = row.split(',')
    if len(row[2]) != 0:
        dateTime = row[1]
        levels[dateTime] = row[2]
    if len(row[6]) != 0:
        dateTime = row[1]
        flows[dateTime] = row[6]

### Adding the predictions to the nowLevel and nowFlow tables

# Adding the values of latest predictions 
for key, value in levels.iteritems():
    queryLevel = "INSERT INTO `nowLevel` (`date`, `Level`) VALUES('{0}', '{1}') ON DUPLICATE KEY UPDATE Level={1}".format(key, value)
    connection.execute(queryLevel)

for key, value in flows.iteritems():
    queryFlow = "INSERT INTO `nowFlow` (`date`, `Flow`) VALUES('{0}', '{1}') ON DUPLICATE KEY UPDATE Flow={1}".format(key, value)
    connection.execute(queryFlow)


print datetime.datetime.now()
print "---end of run---"




# 
# 
# 
# 
# 
# 
# 
# 
# 
# CREATE TABLE `nowLevel` (
#   `date` varchar(30) NOT NULL,
#   `Level` float(5,3) NOT NULL,
#   PRIMARY KEY (`date`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# 
# 
# CREATE TABLE `nowFlow` (
#   `date` varchar(30) NOT NULL,
#   `Flow` float(8,3) NOT NULL,
#   PRIMARY KEY (`date`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
# 
