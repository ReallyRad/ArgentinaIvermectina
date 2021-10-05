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

cases = pd.read_csv("casos confirmados.csv", encoding='utf-8')
# cases = pd.read_csv("covid19casos short.csv", encoding='latin-1')

ivm = pd.read_csv("IVMx1000.csv")

provinces = cases["carga_provincia_nombre"].unique()
provinces.sort()

cfrs = {}
for provincia in provinces :
  old_folks =  cases.loc[cases["edad"] > 0 ]
  old_folks_after_january = old_folks.loc[pd.to_datetime(old_folks["fecha_apertura"]) > pd.to_datetime("2020-07-01")]
  # value_counts = old_folks_after_january.loc[old_folks_after_january["carga_provincia_nombre"] == provincia]["fallecido"].value_counts()
  value_counts = old_folks_after_january.loc[old_folks_after_january["carga_provincia_nombre"] == provincia]["fallecido"].value_counts()
  if "SI" in value_counts.index:
    cfrs[provincia] = value_counts["SI"]/value_counts["NO"]

cfrs = pd.Series(cfrs)
ivm["sum"] = ivm.sum(axis = 1)
ivm.sort_values(["STATE", "sum"])
cfrs = cfrs.sort_index()
scatter = plt.scatter(ivm["sum"], cfrs)
plt.xlabel("IVM x 1000 habitants")
plt.ylabel("CFR")
for i,province in enumerate(provinces):
  plt.annotate(province, (ivm["sum"][i].item(), cfrs[i].item()))

lr = LinearRegression()
lr.fit(ivm["sum"].values.reshape(-1, 1), cfrs.values.reshape(-1, 1))
cfrs_pred = lr.predict(ivm["sum"].values.reshape(-1, 1))

r, p = scipy.stats.pearsonr(ivm["sum"], cfrs)
fitting = polyfit(ivm["sum"], cfrs, 1)

plt.plot(ivm["sum"].values.reshape(-1, 1), cfrs_pred, color="red")
plt.title("CFR x Achats IVM en Argentine par région, a partir de Juillet 2020 "
          + 'Pearson R = '+ str(r) + ', p = ' + str(p) )



plt.show()

x=3

