import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import scipy.stats
import plotly_express as px
# Polynomial Regression
import utils

def polyfit(x, y, degree):
  results = {}

  coeffs = np.polyfit(x, y, degree)

  # Polynomial Coefficients
  results['polynomial'] = coeffs.tolist()

  # r-squared
  p = np.poly1d(coeffs)
  # fit values, and mean
  yhat = p(x)  # or [p(z) for z in x]
  ybar = np.sum(y) / len(y)  # or sum(y)/len(y)
  ssreg = np.sum((yhat - ybar) ** 2)  # or sum([ (yihat - ybar)**2 for yihat in yhat])
  sstot = np.sum((y - ybar) ** 2)  # or sum([ (yi - ybar)**2 for yi in y])
  results['determination'] = ssreg / sstot

  return results

ivm_per_1000_per_region_per_month = pd.read_csv("data/IVMx1000.csv")
cfr_per_region_per_month = pd.read_csv("data/cfr_per_month_per_region.csv")
cases_per_region_per_month_per_1000 = pd.read_csv("data/cases_per_month_per_region_per_1000_inhabitants.csv")

merged = dict()
merged_row = 0
for index, ivm_row in ivm_per_1000_per_region_per_month.iterrows():
    for row_index, ivm_row_value in ivm_row.items():
        if row_index != "STATE" and row_index != "05/2021":
            cfr_value = cfr_per_region_per_month.loc[cfr_per_region_per_month["STATE"] == ivm_row["STATE"]][row_index].values[0]
            cases_per_1000_value = cases_per_region_per_month_per_1000.loc[cases_per_region_per_month_per_1000["STATE"] == ivm_row["STATE"]][row_index].values[0]
            merged[merged_row] = {"STATE": ivm_row["STATE"], "MONTH": row_index, "IVM": ivm_row_value, "CFR": cfr_value, "CASES": cases_per_1000_value}
            merged_row += 1

merged_df = pd.DataFrame.from_dict(merged, orient="index")

merged_df["IVM/CASE"] = merged_df["IVM"]/merged_df["CASES"]

merged_df.replace([np.inf, -np.inf], np.nan, inplace=True)
merged_df.dropna(subset=["IVM/CASE"], how="all")
merged_df["MONTH"] = pd.to_datetime(merged_df["MONTH"])
merged_df = merged_df[merged_df["CFR"]!=0]

merged_df.to_csv("data/merged_dataset.csv")

#merged_df = merged_df[(merged_df['MONTH'] < '2021-01-01')]
#merged_df = merged_df[(merged_df['MONTH'] > '2020-09-01')]
#merged_df = merged_df[merged_df['STATE'].isin(["SALTA","TUCUMAN","JUJUY","MISIONES","LA PAMPA","CORRIENTES"])]

ivm_cfr_df = pd.DataFrame({'ivm':np.array(merged_df["IVM"]), 'cfr':np.array(merged_df["CFR"])})
ivm_cfr_df = ivm_cfr_df[ivm_cfr_df["cfr"]!=0]

r, p = scipy.stats.pearsonr(np.log(ivm_cfr_df["ivm"]), np.log(ivm_cfr_df["cfr"]))

fit = polyfit(np.log(ivm_cfr_df["ivm"]), np.log(ivm_cfr_df["cfr"]), 1)

fig = px.scatter(merged_df, x="IVM",
                 y="CFR",
                 title="CFR x IVM Purchases, " + 'Pearson R = '+ str(r) + ', p = ' + str(p),
                 color="STATE",
                 hover_data=["MONTH", "STATE"],
                 size="CASES",
                 trendline="ols",
                 trendline_scope="overall",
                 trendline_options=dict(log_x=True, log_y=True),
                 log_x=True,
                 log_y=True
                 )

results = px.get_trendline_results(fig)
print(results)

fig.show()
