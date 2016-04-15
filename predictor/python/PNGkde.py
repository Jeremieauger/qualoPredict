# -*- coding: utf-8 -*-
from __future__ import unicode_literals
### The inclusions ###
import os
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from datetime import datetime
from connector import *
### /inclusions ###

### Global variables initialization ###
features = ['Station', 'IP3', 'Ecoli']

# Retrieving allData from DB
dataRequest = 'SELECT {} FROM `AllData`'.format(", ".join(features))
getAll = connection.execute(dataRequest)
allData = DataFrame(getAll.fetchall())
allData.columns = getAll.keys()
Stations = set(allData['Station'])

saveDir = "{}php/kde".format(os.environ.get('OPENSHIFT_REPO_DIR'))

if not os.path.exists(saveDir):
    os.makedirs(saveDir)

'''
allData = pd.read_csv('~/Documents/2013-20XX-Acces-fleuve_org/2015-StageCommunautique/PYTHON/AllData.csv')
'''
#=========================================================================================
# Begin of the main script
#=========================================================================================

x = 'IP3'
y = 'Ecoli'

xMax = max(allData[x])
xMax = 5*(np.ceil(xMax/5))
yMax = max(allData[y])

# Preparing a set of unique observation points from test data list
Stations = set(allData['Station'])
for Station in Stations:
    temp = allData[allData['Station'] == Station]
    fig, ax = plt.subplots()
    plt.title('Station ' + Station + '\nDonnées historiques - Estimation de densité\n')
    plt.subplots_adjust(top = 0.85)
    ax.set_yscale('log')
    plt.ylabel("UFC / 100mL \n (Unités Formatrices de Colonies par 100mL)")
    plt.xlabel(x + " (Indice de Pluie 3 jours) en mm")
    
    ax.set_xlim([-5,xMax])
    ax.set_ylim([1,yMax])
    ax.patch.set_facecolor('#e6e6e6')
    
    xValues = np.array(temp[x])
    yValues = np.array(temp[y])
    
    # Making the horizontal lines
    thresRed = 1000
    thresYellow = 200
    ax.axhline(y=thresRed, linestyle='-', linewidth=3, color='#ff0000', alpha=.5)
    ax.axhline(y=thresYellow, linestyle='-', linewidth=5, color='#ffff00', alpha=.5)
    
    # Calculate the point density
    xy = np.vstack([xValues, yValues])
    z = gaussian_kde(xy)(xy)
    
    ax.scatter(xValues, yValues, c=z, s=100, alpha=.8, edgecolor='')
    
    redI = [ i for i, val in enumerate(yValues) if val>=thresRed ]
    yellowI = [ i for i, val in enumerate(yValues) if val>=thresYellow and val<thresRed ]
    greenI = [ i for i, val in enumerate(yValues) if val<thresYellow ]
    percGreen = round(100.0 * len(greenI) / len(xValues))
    percYellow = round(100.0 * len(yellowI) / len(xValues))
    percRed = round(100.0 * len(redI) / len(xValues))
    muTot = round(np.mean(temp[y]))
    mu0i = [ i for i, val in enumerate(xValues) if val == 0 ]
    mu0 = round(np.mean([ yValues[i] for i in mu0i ]))
    
    legendStr = " Nombre d'échantillonnages : n={0}  \n Moins de 200 : {1}% \n Entre 200 et 1000 : {2}% \n 1000 et plus : {3}% \n Moyenne totale : {4} UFC/100mL \n Moyenne sans pluie : {5} UFC/100mL".format(len(xValues), int(percGreen), int(percYellow), int(percRed), int(muTot), int(mu0))
    props = dict(boxstyle='round,pad=0.6', facecolor='white', alpha=0.8)
    ax.text(0.97, 0.96, legendStr, transform=ax.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='right', bbox=props)

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

