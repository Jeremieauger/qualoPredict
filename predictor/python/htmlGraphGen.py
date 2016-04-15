### The inclusions ###
import os
import numpy as np
import pandas as pd
import mpld3
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
### /inclusions ###

### Global variables initialization ###
features = ['Station', 'IP3', 'Ecoli']
'''
# Getting the environ DB info
user = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME')
passwd = os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD')
host = os.environ.get('OPENSHIFT_MYSQL_DB_HOST')
port = os.environ.get('OPENSHIFT_MYSQL_DB_PORT')

# Connecting to the database
engineString = "mysql://{0}:{1}@{2}:{3}/".format(user, passwd, host, port) 
engine = create_engine(engineString)
connection = engine.connect()
database = "appwithdb"
connectDB = connection.execute("use {}".format(database))

# Retrieving allData from DB
dataRequest = 'SELECT {} FROM `AllData`'.format(", ".join(features))
allData = pd.read_sql_query(dataRequest, connection)
'''
allData = pd.read_csv('~/Documents/2013-20XX-Acces-fleuve_org/2015-StageCommunautique/PYTHON/AllData.csv')

#=========================================================================================
# Begin of the main script
#=========================================================================================

x = 'IP3'
y = 'Ecoli'

xMax = max(allData[x])
xMax = 5*(np.ceil(xMax/5))
yMax = np.log10(max(allData[y]))
yMax = 0.5*(np.ceil(yMax/0.5))

# Preparing a set of unique observation points from test data list
Stations = set(allData['Station'])
for Station in Stations:
    temp = allData[allData['Station'] == Station]
    
    fig, ax = plt.subplots()
    plt.title('Historical Data for: ' +Station+ '\n')
    plt.ylabel("log(" + str(y) + ")")
    plt.xlabel(x)
    
    xLim = [-5,xMax]
    yLim = [0,yMax]
    
    ax.set_xlim([-5,xMax])
    ax.set_ylim([0,yMax])
    ax.patch.set_facecolor('#e6e6e6')
    
    xValues = np.array(temp[x])
    yValues = np.array(np.log10(temp[y]))
    
    thresRed = 3 #log10 of 1000
    thresYellow = np.log10(200)
    
    ax.plot(xLim, [thresRed, thresRed], color="red", lw=3, alpha=0.5)
    ax.plot(xLim, [thresYellow, thresYellow], color="yellow", lw=5, alpha=0.5)
    
    #Selecting and displaying the markers, color according to group
    redI = [i for i, val in enumerate(yValues) if val>=thresRed]
    redX, redY = xValues[redI], yValues[redI]
    ax.scatter(redX, redY, color='#ff0000', alpha=0.5, s=100)
    
    yellowI = [i for i, val in enumerate(yValues) if val>=thresYellow and val<thresRed]
    yellowX, yellowY = xValues[yellowI], yValues[yellowI]
    ax.scatter(yellowX, yellowY, color='#ffff00', alpha=0.5, s=100)
    
    greenI = [i for i, val in enumerate(yValues) if val<thresYellow]
    greenX, greenY = xValues[greenI], yValues[greenI]
    ax.scatter(greenX, greenY, color='#00cc00', alpha=0.5, s=100)
    
    fileName = "../figHTML/" + Station + ".html"
    mpld3.save_html(fig, fileName, )



