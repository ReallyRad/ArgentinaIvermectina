import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import scipy.stats


# Polynomial Regression
def polyfit(x, y, degree):
    results = {}

    coeffs = np.polyfit(x, y, degree)

    # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = np.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot

    return results

ivm_per_1000_per_region_per_month = pd.read_csv("data/IVMx1000.csv")
cfr_per_region_per_month = pd.read_csv("data/regions.csv")

ivm_array = []
cfr_array = []

for month in ivm_per_1000_per_region_per_month.columns:
    if month != "STATE" and month in cfr_per_region_per_month.columns:
        ivm_array.extend(ivm_per_1000_per_region_per_month[month].values)
        cfr_array.extend(cfr_per_region_per_month[month].values)

#scatter = plt.scatter(ivm_array, cfr_array)

ivm_cfr_df = pd.DataFrame({'ivm':np.array(ivm_array), 'cfr':np.array(cfr_array)})
ivm_cfr_df = ivm_cfr_df[ivm_cfr_df["cfr"]!=0]

r, p = scipy.stats.pearsonr(np.log(ivm_cfr_df["ivm"]), np.log(ivm_cfr_df["cfr"]))
#r, p = scipy.stats.pearsonr(np.log(np.array(ivm_array)), np.log(np.array(cfr_array)))
fitting = polyfit(ivm_array, cfr_array, 2)

scatter = plt.scatter(ivm_cfr_df["ivm"], ivm_cfr_df["cfr"])

plt.xlabel("IVM x 1000 inhabitants")
plt.ylabel("CFR")
plt.xscale('log')
plt.yscale('log')
plt.title("CFR x Achats IVM en Argentine par région, a partir de Juillet 2020 "
          + 'Pearson R = '+ str(r) + ', p = ' + str(p) )
plt.show()

x=3