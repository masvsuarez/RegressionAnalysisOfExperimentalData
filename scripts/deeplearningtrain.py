import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.optimizers import Adam

from sklearn.metrics import r2_score
# from sklearn.model_selection import StratifiedKFold # don't use stratifiedkfold cause it's only for classifications
from sklearn.model_selection import KFold


import statistics

# defining the Keras model

model = Sequential()
model.add(Dense(8,input_dim = 1024, activation = 'relu')) # input_dim is 1024 since we're using 1024 bitvectors, 
                                                            # 8 is the number of nodes in the first hidden layer
model.add(Dropout(0.5))

model.add(Dense(1,activation = 'relu')) # this is the output layer, it only has 1 node because we only want pIC50 as output

#from keras.optimizers import Adam
opt = Adam(learning_rate=0.1,beta_1 = 0.9)
model.compile(optimizer = opt, loss = 'mean_squared_error') # configuring the model's learning process

training_data = pickle.load(open('assay8_training_data_1.df','rb'))
test_data = pickle.load(open('assay8_test_data_1.df','rb'))

# preparing the dataset for the model
X_train = training_data['fp_bitvect'] # input data
y_train = training_data['pIC50'] # output data

# convert dataset to numpy array because the model is compatible with it
X_train_array = np.array(list(X_train)) 
y_train_array = np.array(list(y_train))

# preparing the test dataset for the model
X_test = test_data['fp_bitvect'] # input data
y_test = test_data['pIC50'] # output data

# convert dataset to numpy array because the model is compatible with it
X_test_array = np.array(list(X_test)) 
y_test_array = np.array(list(y_test))

model.count_params()

# fitting the model on the dataset
nn = model.fit(X_train_array, y_train_array, epochs = 75, batch_size = 64, validation_data = (X_test_array, y_test_array))
