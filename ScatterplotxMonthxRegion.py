import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import scipy.stats
import seaborn as sns
import plotly_express as px
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

cfr_per_region_per_month = pd.read_csv("data/cfr_per_month_per_region.csv")

merged = dict()
merged_row = 0
for index, ivm_row in ivm_per_1000_per_region_per_month.iterrows():
    for row_index, ivm_row_value in ivm_row.items():
        if row_index != "STATE" and row_index != "05/2021":
            cfr_value = cfr_per_region_per_month.loc[cfr_per_region_per_month["STATE"] == ivm_row["STATE"]][row_index].values[0]
            merged[merged_row] = {"STATE": ivm_row["STATE"], "MONTH": row_index, "IVM": ivm_row_value, "CFR": cfr_value}
            merged_row += 1

merged_df = pd.DataFrame.from_dict(merged, orient="index")

ivm_cfr_df = pd.DataFrame({'ivm':np.array(merged_df["IVM"]), 'cfr':np.array(merged_df["CFR"])})
ivm_cfr_df = ivm_cfr_df[ivm_cfr_df["cfr"]!=0]

r, p = scipy.stats.pearsonr(np.log(ivm_cfr_df["ivm"]), np.log(ivm_cfr_df["cfr"]))

fig = px.scatter(merged_df, x="IVM",
                 y="CFR",
                 title="CFR x IVM Purchases, " + 'Pearson R = '+ str(r) + ', p = ' + str(p),
                 color="MONTH",
                 hover_data=["MONTH", "STATE"],
                 log_x=True,
                 log_y=True)

fig.show()
