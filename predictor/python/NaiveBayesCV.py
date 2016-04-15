### The inclusions
import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix

### Global variables initialization
features = ['IP3','MeanTemp','Flow','Level']
#'IP3','MeanTemp','Flow','Level'
predFeature = 'Ecoli'
nbCV = 2
models = {}
matrix_GLOB = np.zeros((3, 3))
TP_R_1_GLOB = 0
TP_R_2_GLOB = 0
TP_R_3_GLOB = 0
TP_R_tot_GLOB = 0
allData=pd.read_csv('AllData.csv')
#allData=pd.read_csv('/Users/jay/Documents/2013-20XX-Acces-fleuve_org/2015-StageCommunautique/AllData.csv')

### Functions
def predict(Station, conditions):
    if Station in models:
        model = models[Station]
    else:
        temp = train[train['Station'] == Station]
        x = temp[list(features)].values
        y = temp[predFeature].values
        # model = GaussianNB()
        model = MultinomialNB()
        model.fit(x, y)
        models.update({Station: model})
    predicted = model.predict([conditions])
    return predicted[0]

def confusionMatrix(y_true, y_pred):
    if (len(y_true) != len(y_pred)): 
        print("Lists compared must be of same length!")
        return -1
    matrix = np.zeros((3, 3))
    for i in range(1,len(y_pred)):
        matrix[int(y_true[i])-1][int(y_pred[i])-1] +=1 
    TP_R_1 = 0 
    TP_R_2 = 0
    TP_R_3 = 0
    if (matrix[0][0]+matrix[1][0]+matrix[2][0] == 0):TP_R_1 = 0
    else : TP_R_1 = (float(matrix[0][0])/(float(matrix[0][0]+matrix[1][0]+matrix[2][0])))
    if (matrix[0][1]+matrix[1][1]+matrix[2][1] == 0): TP_R_2 = 0
    else : TP_R_2 = (float(matrix[1][1])/(float(matrix[0][1]+matrix[1][1]+matrix[2][1])))
    if (matrix[0][2]+matrix[1][2]+matrix[2][2] == 0): TP_R_2 = 0
    else : TP_R_3 = (float(matrix[2][2])/(float(matrix[0][2]+matrix[1][2]+matrix[2][2])))
    TP_R_tot = float(matrix[0][0]+matrix[1][1]+matrix[2][2])/len(y_true)
    return (matrix, TP_R_1, TP_R_2, TP_R_3, TP_R_tot)


#=========================================================================================
# Begin of the main script
#=========================================================================================
print("model based on: "),
print(features)
print("predicting: "),
print(predFeature) 


for i in range(0,nbCV):
    print("Cross validation iteration : "+ str(i+1) )
    
    train, test = train_test_split(allData, test_size = 0.3)
    
    # These lines are to make a copy of the dataframes (train, test) instead of slices
    # of the allData df. (and to speed up the following operations and to avoid the warning "A value is trying to be set on a copy of a slice from a DataFrame"
    train = train[:]
    test = test[:]
    
    #Create a flag for Train and Test Data set
    #train.loc[:,'Type']='Train'
    #test.loc[:,'Type']='Test'
    
    # Preparing a set of unique observation points from test data list
    observations = test[['Station','Date']]
    
    # Iterating through the test's unique tuples (Station+Date) to get the conditions and predict
    for row in observations.itertuples():
        temp = test[(test.Station == row[1]) & (test.Date == row[2])]
        #conditions = [temp.IP3.values[0],temp.MeanTemp.values[0],temp.Level.values[0]]
        conditions = temp[list(features)].values[0]
        test.loc[row[0],'Prediction'] = predict(temp.Station.values[0],conditions)
    
    
    # Categorizing the predicted Ecoli outcome 
    for row in test.itertuples():
        if (row.Prediction < 200): 
            test.loc[row[0],'PredNum'] = np.int64(1)
        elif (row.Prediction < 1000): 
            test.loc[row[0],'PredNum'] = np.int64(2)
        else : 
            test.loc[row[0],'PredNum'] = np.int64(3)
    
    # Creating the arrays to build the confusion matrix
    y_true = np.array(test.QualNum.values, dtype=object)
    y_pred = np.array(test.PredNum.values, dtype=object)
    
    # Calculating the confusion matrix and some associated metrics    
    (matrix, TP_R_1, TP_R_2, TP_R_3, TP_R_tot) = confusionMatrix(y_true, y_pred)
    cm = confusion_matrix(y_true.astype('int'), y_pred.astype('int'))
    print(cm)
    # Summing the calculated values
    matrix_GLOB += matrix
    TP_R_1_GLOB += TP_R_1
    TP_R_2_GLOB += TP_R_2
    TP_R_3_GLOB += TP_R_3
    TP_R_tot_GLOB += TP_R_tot
    # Re-initializing the models, they have to be recalculated from "train" each iteration
    models = {}

matrix_GLOB = matrix_GLOB

# Displaying the 
print("\n--- Cross validations completed ---")

print("--Predicted class--> \n"+str(matrix_GLOB[0])+"\n"+str(matrix_GLOB[1])+"\n"+str(matrix_GLOB[2]))

print("Accuracy for 1:\t"+str(TP_R_1_GLOB/nbCV))
print("Accuracy for 2:\t"+str(TP_R_2_GLOB/nbCV))
print("Accuracy for 3:\t"+str(TP_R_3_GLOB/nbCV))
print("Global accuracy:\t"+str(TP_R_tot_GLOB/nbCV))

