"""
Performs Partial Least Squares on a subset of the data to perform cross-validation and obtain an R^2 score
!!! Outdated implementation
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

#fits and scores the optimised pls model and returns predicted Y and an R2 score
def plsfinal(trainX, trainY, testX, testY, i):
    plsModel = PLSRegression(n_components=i)
    plsModel.fit(trainX,trainY)
    pred_Y = plsModel.predict(testX)
    R2 = plsModel.score(testX, testY)
    return pred_Y, R2

#plsfinal(data_trainX,data_trainY, data_testX, data_testY,4)

#loop to evaluate R2 array for train/test split of the PLS data

R2_collection = np.array([])
for i in range(0,196):
    filename1 = 'PLS_input/Col' + str(i) + 'ExpTrain'
    filename2 = 'PLS_input/Col' + str(i) + 'ExpTest'
    data = np.loadtxt(filename1, delimiter=',', skiprows=1)
    data2 = np.loadtxt(filename2, delimiter=',', skiprows=1)
    cmpdindx_train = data[:,0]
    data_trainX = data[:,2:]
    data_trainY = data[:,1]
    cmpdindx_test = data2[:,0]
    data_testX = data2[:,2:]
    data_testY = data2[:,1]
    _, R2 = allpls(data_trainX,data_trainY, data_testX, data_testY)
    R2_collection = np.append(R2_collection, R2)
    if i %10 ==0:
        print(i)
np.savetxt("r2_pls.csv",R2_collection, delimiter=',')