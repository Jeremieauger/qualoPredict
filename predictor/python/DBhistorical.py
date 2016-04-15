### The inclusions ###
import os, re
from os import listdir
from os.path import isfile, join
from sqlalchemy import create_engine
from connector import *
### / inclusions ###

dataPath =  os.environ.get('OPENSHIFT_DATA_DIR') + 'rawData/'
fileNames = [f for f in listdir(dataPath) if isfile(join(dataPath, f))]

# Creating the tables if they don't already exist
sqlCreate = "CREATE TABLE IF NOT EXISTS `Qualo` (`Station` varchar(15) NOT NULL,  `Date` date NOT NULL,  `Temperature` varchar(5),  `Conductivite` int(5),  `pH` varchar(5),  `Signe` varchar(1),  `Ecoli` int(7) NOT NULL,  `MeteoRSMA` int(1),  PRIMARY KEY (`Station`,`date`),  KEY `Station` (`Station`),  KEY `date` (`date`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
dummy = connection.execute(sqlCreate)
sqlCreate = "CREATE TABLE IF NOT EXISTS `MeteoRaw` (`Date` date NOT NULL,`Year` int(4) NOT NULL,`Month` int(2) NOT NULL,`Day` int(2) NOT NULL,`DataQuality` varchar(1),`MaxTemp` float(3,1) NOT NULL,`MaxTempFlag` varchar(1),`MinTemp` float(3,1) NOT NULL,`MinTempFlag` varchar(1),`MeanTemp` float(3,1) NOT NULL,`MeanTempFlag` varchar(1),`HeatDegDays` float(3,1) NOT NULL,`HeatDegDaysFlag` varchar(1),`CoolDegDays` float(3,1) NOT NULL,`CoolDegDaysFlag` varchar(1),`TotalRain(mm)` float(4,1) NOT NULL,`TotalRainFlag` varchar(1),`TotalSnow(mm)` float(4,1) NOT NULL,`TotalSnowFlag` varchar(1),`TotalPrecip(mm)` float(4,1) NOT NULL,`TotalPrecipFlag` varchar(1),`SnowOnGround(cm)` float(4,1) NOT NULL,`SnowOnGroundFlag` varchar(1),`DirMaxGust(10sDeg)` float(4,1) NOT NULL,`DirMaxGustFlag` varchar(1),`SpdOfMaxGust(10sDeg)` float(4,1) NOT NULL,`SpdOfMaxGustFlag` varchar(1),PRIMARY KEY (`Year`,`Month`,`Day`),KEY `Year` (`Year`),KEY `Month` (`Month`),KEY `Day` (`Day`) USING BTREE) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
dummy = connection.execute(sqlCreate)
sqlCreate = "CREATE TABLE IF NOT EXISTS `StationGPS` (`Station` VARCHAR(23) NOT NULL,`Nom` VARCHAR(36) DEFAULT NULL,`Localisation` VARCHAR(200) DEFAULT NULL,`Administration` VARCHAR(40) DEFAULT NULL,`Latitude` FLOAT(10,6) NOT NULL,`Longitude` FLOAT(10,6) NOT NULL,`1999` INT(4) DEFAULT NULL,`2000` INT(4) DEFAULT NULL,`2001` INT(4) DEFAULT NULL,`2002` INT(4) DEFAULT NULL,`2003` INT(4) DEFAULT NULL,`2004` INT(4) DEFAULT NULL,`2005` INT(4) DEFAULT NULL,`2006` INT(4) DEFAULT NULL,`2007` INT(4) DEFAULT NULL,`2008` INT(4) DEFAULT NULL,`2009` INT(4) DEFAULT NULL,`2010` INT(4) DEFAULT NULL,`2011` INT(4) DEFAULT NULL,`2012` INT(4) DEFAULT NULL,`2013` INT(4) DEFAULT NULL,`2014` INT(4) DEFAULT NULL,`2015` INT(4) DEFAULT NULL,PRIMARY KEY (`Station`)) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
dummy = connection.execute(sqlCreate)


# Importing the water quality data (from RSMA, with the header manually removed to avoid accents)
for file in fileNames:
    if re.match(r'qualo\d+\.csv', file):
        query = "LOAD DATA LOCAL INFILE '{0}' INTO TABLE `Qualo` FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'".format(dataPath + file)
        connection.execute(query)

# Importing the meteorological historical data
for file in fileNames:
    if re.match(r'eng-daily-\d+-\d+\.csv', file):
        query = "LOAD DATA LOCAL INFILE '{0}' INTO TABLE `MeteoRaw` FIELDS TERMINATED BY ',' ENCLOSED BY '\"'LINES TERMINATED BY '\n' IGNORE 26 ROWS;".format(dataPath + file)
        connection.execute(query)
# Importing the stations informations
csvName = 'stationsInfo.csv'
query = "LOAD DATA LOCAL INFILE '{0}' INTO TABLE `StationGPS` FIELDS TERMINATED BY ',' ENCLOSED BY '\"'LINES TERMINATED BY '\n' IGNORE 1 ROWS;".format(dataPath + csvName)
connection.execute(query)


