
"""
Plot results
"""

__author__ = "Michael Suarez"
__email__ = "masv@connect.ust.hk"
__copyright__ = "Copyright 2018, Hong Kong University of Science and Technology"
__license__ = "3-clause BSD"

import matplotlib.pyplot as plt
import numpy as np

# modify here number of assays and compounds
no_cmps = 21436
no_assays = 197

filename = 'r2_pls.csv'
data = np.loadtxt(filename, delimiter=',')
data[::-1].sort()
assay = range(1,no_assays)
#filename2 ='r2_rnd.csv'
#data2 = np.loadtxt(filename2, delimiter=',')
#data2[::-1].sort()
#filename3 = 'r2_rfr_ordered_rnd.csv'
#data3 = np.loadtxt(filename3, delimiter=',')
#data3[::-1].sort()

plt.figure(figsize=(12,8))
plt.plot(assay,data,linestyle='',marker='o',markersize=3, label='pQSAR clust, median = %.2f' %clustmed)
#plt.plot(assay,data2,linestyle='',marker='o',markersize=3, label='pQSAR rnd. median = %.2f' %rndmed)
#plt.plot(assay,data3,linestyle='',marker='o',markersize=3, label='RFR rnd. median = %.2f' %rndRFRmed)
plt.hlines(0.3, 0,200)
plt.ylim((0,1))
plt.xlim((0,200))
plt.legend()
plt.show()