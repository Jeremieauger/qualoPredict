### The inclusions ###
import os
import pandas as pd
from sqlalchemy import create_engine
from sklearn.naive_bayes import MultinomialNB
from connector import *
try:
   import cPickle as pickle
except:
   import pickle
### /inclusions ###

### Global variables initialization ###
features = ['IP3','MeanTemp','Flow','Level']
predFeature = 'Ecoli'
models = {}

# Retrieving allData from DB
toSelect = ['Station', predFeature]
toSelect.extend(features)
dataRequest = 'SELECT {} FROM `AllData`'.format(", ".join(toSelect))
allData = pd.read_sql_query(dataRequest, connection)

#=========================================================================================
# Begin of the main script
#=========================================================================================

# Preparing a set of unique observation points from test data list
Stations = set(allData['Station'])

# Making the predictions
for Station in Stations:
    temp = allData[allData['Station'] == Station]
    x = temp[list(features)].values
    y = temp[predFeature].values
    model = MultinomialNB()
    model.fit(x, y)
    models.update({Station: model})

# Saving the models
pickle.dump( models, open( "models.p", "wb" ) )
