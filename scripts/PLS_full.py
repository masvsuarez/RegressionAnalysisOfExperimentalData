
"""
Completes the query data points through a partial least squares regression
"""

__author__ = "Michael Suarez"
__email__ = "masv@connect.ust.hk"
__copyright__ = "Copyright 2018, Hong Kong University of Science and Technology"
__license__ = "3-clause BSD"


from sklearn.model_selection import cross_validate
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_decomposition import PLSRegression
import time

# modify here number of assays and compounds
no_cmps = 21436
no_assays = 197

full = np.loadtxt('data/RFR_full.csv', delimiter=",")
matrx = np.loadtxt("data/total_mastertable_nan.csv", delimiter=",")

#cross validation returns scaled test score penalising large component models Q2 = Q2 - CMP*0.002
def plsregress(trainX, trainY, i):
    plsModel = PLSRegression(n_components=i)
    plsModel.fit(trainX,trainY)
    average_test_score = np.mean(cross_validate(plsModel, trainX,trainY, cv=5)['test_score'])
    scaled_test_score = average_test_score - (0.002*i)
    average_test_score_std = np.std(cross_validate(plsModel, trainX,trainY, cv=5)['test_score'])
#    print('Number of components: %d' % i)
#    print('Val score: %f' %scaled_test_score,average_test_score, average_test_score_std)
    return scaled_test_score,average_test_score, average_test_score_std

#running cross validation over the number of components from 2-25
def optimisingcomp(trainX, trainY):
    test_score = np.array([])
    scaled_test_score = np.array([])
    test_score_std = np.array([])
    for i in range(2, 26):
        scaled_test, average_test, average_test_std = plsregress(trainX, trainY, i)
        scaled_test_score = np.append(scaled_test_score, scaled_test)
        test_score = np.append(test_score, average_test)
        test_score_std = np.append(test_score_std, average_test_std)
        error_array = np.concatenate(([test_score],[test_score_std]), axis=0)
        error_array = np.concatenate(([scaled_test_score],error_array), axis=0)
    return error_array

#error_array = optimisingcomp(data_trainX,data_trainY)

#fits and scores the optimised pls model and returns predicted Y 
def plsfinal(trainX, trainY, toPX, i):
    plsModel = PLSRegression(n_components=i)
    plsModel.fit(trainX,trainY)
    pred_Y = plsModel.predict(toPX)
    return pred_Y

#plsfinal(data_trainX,data_trainY, data_testX, data_testY,4)


#automates choice of ideal number of components
def allpls(trainX, trainY, toPX):
    error_array = optimisingcomp(trainX, trainY)
    best_comp = np.argmax(error_array, axis=1)[0]+2
    pred_Y= plsfinal(trainX, trainY, toPX, best_comp)
    return pred_Y


#loop to evaluate full matrix
Y_collection = np.empty(shape=(no_cmps,no_assays))
for i in range(no_assays):
    pos_hits = np.where(~np.isnan(matrx[:,i]))[0]
    EXPY = matrx[pos_hits,i]
    EXPX = full[pos_hits]
    EXPX = np.delete(EXPX, i, axis=1)
    pos_nan = np.where(np.isnan(matrx[:,i]))[0]
    toPX = full[pos_nan]
    toPX = np.delete(toPX, i, axis=1)
    
    pred_Y = allpls(EXPX, EXPY, toPX)
    pred_Y = pred_Y.flatten()
    newY = np.append(pred_Y, EXPY)
    indx = np.append(pos_nan,pos_hits)
    newY = newY[indx.argsort()]
    Y_collection[:,i]=newY

np.savetxt("data/PLSfull.csv",Y_collection, delimiter=',')