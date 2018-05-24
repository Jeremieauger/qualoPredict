import os, re, datetime, requests
from sqlalchemy import create_engine
from lxml import html
from connector import *

# Determining the URL / name of the most recent NowCast matrix
index = requests.get('http://dd.weather.gc.ca/nowcasting/matrices/')
indexTree = html.fromstring(index.content)
names = indexTree.xpath('//a')
fileNames = []
for name in names:
    name = name.text
    if re.match(r'.*\d\d.*', name):
        fileNames.append(name)

### Adding the predictions to the nowRainAndTemp table

for filename in fileNames:
    # Downloading the .Z archive and saving to file
    URL = "http://dd.weather.gc.ca/nowcasting/matrices/{0}".format(filename)
    dataDir = os.environ.get('OPENSHIFT_DATA_DIR')
    pathToZIP = ''.join([dataDir, filename])
    command = "rm {}SCRIBE.*".format(dataDir)
    os.system(command)
    command = "wget -q -O {0} {1}".format(pathToZIP, URL)
    os.system(command)

    # Decompressing and opening the downloaded meteo predictions
    command = 'gzip -d {}'.format(pathToZIP)
    os.system(command)
    fileHandle = filename[:-2]
    pathToFile = '/'.join([dataDir, fileHandle])
    f = open(pathToFile)
    docString = f.read()
    matrices = docString.split("\n.\n")

    # Parsing and isolating the matrix for the montreal prediction (at P-E Trud. Airport)
    for matrix in matrices:
        if re.match(r'^STN: CYUL', matrix):
            mtlMeteo = matrix.split("\n")

    # Calculating the TOTAL RAIN for the next 12 hours (skipping current hour to have 12)
    i = 0 #to skip the first 3 lines of information
    rain12h = 0.0
    for row in mtlMeteo:
        elements = row.split("|")
        if len(elements) == 1:
            i += 1
        if i > 3:
            if len(elements) > 15:
                rain12h += float(elements[10])

    rain24h = rain12h * 2

    # Calculating the MEAN TEMP for the next 12 hours (skipping current hour to have 12)
    i = 0
    temp12h = 0.0
    for row in mtlMeteo:
        elements = row.split("|")
        if len(elements) == 1:
            i += 1
        if i > 3:
            if len(elements) > 15:
                temp12h += float(elements[12])

    meanTemp = temp12h/12

    # Formating the date time stamp to match the FlowAndLevel's stamp -yyyy-MM-ddThh:mm:ssZ (time info taken from file name)
    fileNames = filename.split(".")[2:5]
    fileNames[2] = fileNames[2][:-1]  
    (month, day, hour) = fileNames
    year = datetime.datetime.now().year
    date = "{0}-{1}-{2}T{3}:00:00-05:00".format(year, month, day, hour)

    # Adding the values of latest predictions 
    queryRainAndTemp = "INSERT INTO `nowRainAndTemp` (`date`, `rain24h`, `meanTemp`) VALUES('{0}', '{1}', '{2}') ON DUPLICATE KEY UPDATE rain24h={1}, meanTemp={2}".format(date, rain24h, meanTemp, )
    connection.execute(queryRainAndTemp)


