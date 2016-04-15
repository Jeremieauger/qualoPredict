# -*- coding: utf-8 -*-
from __future__ import unicode_literals
### The inclusions ###
import os
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime
from connector import *
### /inclusions ###

### Global variables initialization ###
features = ['Station', 'Date', 'Ecoli']

def set1900(date):
    return date.replace(year=1900)

# Retrieving allData from DB
dataRequest = 'SELECT {} FROM `AllData`'.format(", ".join(features))
getAll = connection.execute(dataRequest)
allData = DataFrame(getAll.fetchall())
allData.columns = getAll.keys()
Stations = set(allData['Station'])

saveDir = "{}php/seasonal".format(os.environ.get('OPENSHIFT_REPO_DIR'))

if not os.path.exists(saveDir):
    os.makedirs(saveDir)

'''
allData = pd.read_csv('~/Documents/2013-20XX-Acces-fleuve_org/2015-StageCommunautique/PYTHON/AllData.csv')
'''
#=========================================================================================
# Begin of the main script
#=========================================================================================

x = 'Date'
y = 'Ecoli'

yMax = max(allData[y])

# Preparing a set of unique observation points from test data list
Stations = set(allData['Station'])
for Station in Stations:
    temp = allData[allData['Station'] == Station]
    fig, ax = plt.subplots()
    plt.title('Données Saisonnières pour: ' + Station + '\n')
    ax.set_yscale('log')
    plt.ylabel("UFC / 100mL \n (Unités Formatrices de Colonies par 100mL)")
    plt.xlabel("Mois de l'année (toutes années confondues)")
    
    xMin = datetime.strptime('1900-04-15', '%Y-%m-%d')
    xMax = datetime.strptime('1900-11-01', '%Y-%m-%d')
    ax.set_xlim([xMin,xMax])
    ax.set_ylim([1,yMax])
    ax.patch.set_facecolor('#e6e6e6')
    
    xValues = np.array(map(set1900,temp[x]))
    yValues = np.array(temp[y])
    myFmt = mdates.DateFormatter('%b')
    ax.xaxis.set_major_formatter(myFmt)
    
    # Making the horizontal lines
    thresRed = 1000
    thresYellow = 200
    ax.axhline(y=thresRed, linestyle='-', linewidth=3, color='#ff0000', alpha=.5)
    ax.axhline(y=thresYellow, linestyle='-', linewidth=5, color='#ffff00', alpha=.5)
    
    # Selecting and displaying the markers, color according to group
    redI = [ i for i, val in enumerate(yValues) if val>=thresRed ]
    redX = [ xValues[i] for i in redI ]
    redY = [ yValues[i] for i in redI ]
    ax.plot(redX, redY, linestyle='none', color='#ff0000', alpha=0.9, ms=10, marker='o')
    
    yellowI = [ i for i, val in enumerate(yValues) if val>=thresYellow and val<thresRed ]
    yellowX = [ xValues[i] for i in yellowI ]
    yellowY = [ yValues[i] for i in yellowI ]
    ax.plot(yellowX, yellowY, linestyle='none', color='#ffff00', alpha=0.9, ms=10, marker='o')
    
    greenI = [ i for i, val in enumerate(yValues) if val<thresYellow ]
    greenX = [ xValues[i] for i in greenI ]
    greenY = [ yValues[i] for i in greenI ]
    ax.plot(greenX, greenY, linestyle='none', color='#00cc00', alpha=0.9, ms=10, marker='o')
    
    plt.annotate(
        "seuil 200",
        xy = (xMax, 200), xytext = (40, 0),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 1))
    
    plt.annotate(
        "seuil 1000",
        xy = (xMax, 1000), xytext = (40, 0),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'red', alpha = 1))
    
    fileName = saveDir + "/" + Station + ".png"
    plt.savefig(fileName)
    plt.close()

