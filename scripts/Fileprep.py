
"""
Prepares files for future steps 
!!! outdated - TODO fix it
"""

__author__ = "Michael Suarez"
__email__ = "masv@connect.ust.hk"
__copyright__ = "Copyright 2018, Hong Kong University of Science and Technology"
__license__ = "3-clause BSD"

import pandas as pd
import numpy as np

file_name = 'ChEMBL_data_copy.xlsx'
sheet = 'CLcpd_train' # (A,C,P)xN dimensional list 
pci50 = pd.read_excel(io=file_name, sheet_name=sheet, usecols=[3,4,5])
#smiles = pd.read_excel(io=file_name, sheet_name='cpd_list', usecols=[4])
matches = pd.DataFrame(pci50)

#sheet2 = 'cpd_list' # 1xC dimensional list of all CompoundID
#cmpID = pd.read_excel(io=file_name, sheet_name=sheet2, usecols=0)
#cmpID_key = pd.DataFrame(cmpID)

#sheet3 = 'assay_meta_data' # 1xA dimensional list of all AssayID
#assID = pd.read_excel(io=file_name, sheet_name=sheet3, usecols=[6])
#assID_key = pd.DataFrame(assID)

#csv version for the new Database
file_name = 'trainingActivities.csv'

# (P,A,C)xN dimensional list 
pci50 = pd.read_csv(file_name, usecols=[2,3,4])
matches = pd.DataFrame(pci50)
no_rows = 100492 #excel rows minus 1 (for header)

file_name2 = 'testActivities.csv'
# (P,A,C)xN dimensional list 
pci502 = pd.read_csv(file_name2, usecols=[2,3,4])
matches2 = pd.DataFrame(pci502)
no_rows2 = 31688 #excel rows minus 1 (for header)


##create mastertables for PLS calculation

#matches.columns #value search given item location in 3xN matrix |  PCI50,Assay IDX, Cmpd IDX
mastertable = np.zeros([21389,197])
for i in range(no_rows): #number of matches
    mastertable[matches.iat[i,2],matches.iat[i,1]]=matches.iat[i,0]
mastertable = mastertable[1:,1:]
    
mastertable2 = np.zeros([21389,197])
for i in range(no_rows2): #number of matches
    mastertable2[matches2.iat[i,2],matches2.iat[i,1]]=matches2.iat[i,0]
mastertable2 = mastertable2[1:,1:]

#sum together
mastertable3 = mastertable+mastertable2
mastertable3[mastertable3==0]='nan'
np.savetxt("total_mastertable_nan.csv", mastertable3, delimiter=",")
#train data
mastertable[mastertable==0]='nan'
np.savetxt("train_mastertable_nan.csv", mastertable, delimiter=",")
#test data
mastertable2[mastertable2==0]='nan'
np.savetxt("test_mastertable_nan.csv", mastertable2, delimiter=",")


#ID if clustered - csv version for the new Database
file_name = 'trainingActivities.csv'

# (P,A,C)xN dimensional list 
pci50 = pd.read_csv(file_name, usecols=[2,3,4])
matches = pd.DataFrame(pci50)
no_rows = 100492 #excel rows minus 1 (for header)

file_name2 = 'testActivities.csv'
# (P,A,C)xN dimensional list 
pci502 = pd.read_csv(file_name2, usecols=[2,3,4])
matches2 = pd.DataFrame(pci502)
no_rows2 = 31688 #excel rows minus 1 (for header)


##create mastertables for PLS calculation

#matches.columns #value search given item location in 3xN matrix |  PCI50,Assay IDX, Cmpd IDX
mastertable = np.zeros([21389,197])
for i in range(no_rows): #number of matches
    mastertable[matches.iat[i,2],matches.iat[i,1]]=matches.iat[i,0]
mastertable = mastertable[1:,1:]
    
mastertable2 = np.zeros([21389,197])
for i in range(no_rows2): #number of matches
    mastertable2[matches2.iat[i,2],matches2.iat[i,1]]=matches2.iat[i,0]
mastertable2 = mastertable2[1:,1:]


#train data 
mastertable[mastertable!=0]=1
#test data
mastertable2[mastertable2!=0]=2
#sum together
mastertable3 = mastertable+mastertable2
mastertable3[mastertable3==0]='nan'
ID = np.array([range(0,21388)])
ID = np.transpose(ID)
mastertable3 = np.append(mastertable3,ID,axis=1)
np.savetxt("ID_mastertable_nan.csv", mastertable3, delimiter=",")

