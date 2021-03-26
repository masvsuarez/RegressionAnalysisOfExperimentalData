
"""
Performs Random Forest Regression on the sparse data matrix
"""

__author__ = "Michael Suarez"
__email__ = "masv@connect.ust.hk"
__copyright__ = "Copyright 2018, Hong Kong University of Science and Technology"
__license__ = "3-clause BSD"

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from rdkit.Chem.AllChem import  GetMorganFingerprintAsBitVect, GetErGFingerprint
from rdkit import Chem
from rdkit.Chem import AllChem

# modify here number of assays and compounds
no_cmps = 21436
no_assays = 197

cmpds = pd.read_csv("data/CMPDSMILES.csv")
matrx = np.loadtxt("data/total_mastertable_nan.csv", delimiter=",")

def molfromsmiles(mol):
    return Chem.MolFromSmiles(mol)
cmpds['mol'] = cmpds['canonical_smiles'].apply(molfromsmiles)

def morgfing(mol):
    return AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
cmpds['fp'] = cmpds['mol'].apply(morgfing)

X = np.array(list(cmpds['fp']))

full = np.empty((no_cmps,no_assays))

# fills in sparse data from existing data through RF
for i in range(no_assays):
    pos_hits = np.where(~np.isnan(matrx[:,i]))[0]
    y = matrx[pos_hits,i]
    X_train = X[pos_hits]
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y)
    pred = model.predict(X)
    full[:,i] = pred
    full[pos_hits,i]=y

np.savetxt("data/RFR_full.csv",full, delimiter=',')