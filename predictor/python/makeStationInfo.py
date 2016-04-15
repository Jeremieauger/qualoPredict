# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
from connector import *

StationInfoFile = '{}rawData/stationInfo.json'.format(os.environ.get('OPENSHIFT_REPO_DIR'))
json_data=open(StationInfoFile).read()
data = json.loads(json_data)
# json_data=open('stationInfo.json').read()
# data = json.loads(json_data)

dropQuery = "DROP TABLE IF EXISTS `stationInfo`;"
connection.execute(dropQuery)
createQuery = " CREATE TABLE IF NOT EXISTS `stationInfo` ( `Station` varchar(15) NOT NULL, `Latitude` float(18,16), `Longitude` float(18,16), `DescShort` varchar(50), `DescLong` varchar(250), PRIMARY KEY (`Station`), KEY `Station` (`Station`) USING BTREE ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
connection.execute(createQuery)

Stations = data['features']
for station in Stations:
    Station = station['attributes']['STATIONS']
    Longitude = station['geometry']['x']
    Latitude = station['geometry']['y']
    DescShort = station['attributes']['NOM_RAPPOR']
    DescShort = DescShort.replace("\"", "'")
    DescLong1 = station['attributes']['LOCALISA_1']
    DescLong = station['attributes']['LOCALISA_2']
    DescLong = DescLong.replace("\"", "'")
    if len(DescShort) < 2 :
        DescShort = DescLong.split(',')[0]
    sql = "INSERT INTO `stationInfo` (Station, Latitude, Longitude, DescShort, DescLong) VALUES ('{0}',{1},{2},\"{3}\",\"{4}\");".format(Station, Latitude, Longitude, DescShort, DescLong)
    connection.execute(sql)






