# -*- coding: utf-8 -*-
### The inclusions ###
import os, re, requests, datetime
from sqlalchemy import create_engine
from pandas import DataFrame
from connector import *
### /inclusions ###

# Function to parse the UFC and the dates, keeping only desired characters
def parser(str):
    return ''.join([s for s in list(str) if s.isdigit() or s == '-' ])

#Getting the names from all the active stations
getAll = connection.execute('SELECT Station FROM `AllData`')
allData = DataFrame(getAll.fetchall())
allData.columns = getAll.keys()
Stations = set(allData['Station'])

for Station in Stations:
    url = "http://www.rsma.qc.ca/rsmaweb/tableau.asp?s={0}&p=Q".format(Station)
    r = requests.get(url)
    dataLines = re.findall(r'dData.*"D".*\r\n', r.text)
    for line in dataLines:
        date = parser(line.split(',')[1])
        UFC = parser(line.split(',')[5])
            query = "INSERT IGNORE INTO nowQualo (`Station`,`Date`,`UFC`) VALUES ('{0}','{1}','{2}');".format(Station, Date, UFC)
            connection.execute(query)

# Cleaning to avoid having empty entries in the db
sqlDel = "DELETE FROM nowQualo WHERE DATE_FORMAT(Date, '%Y') = '0000';"
connection.execute(sqlDel)
