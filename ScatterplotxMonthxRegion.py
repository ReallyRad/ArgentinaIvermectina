import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import scipy.stats
import plotly_express as px
# Polynomial Regression

ivm_region_month_1000 = pd.read_csv("data/IVMx1000.csv")
cfr_region_month = pd.read_csv("data/cfr_per_month_per_region.csv")
cases_region_month_1000 = pd.read_csv("data/cases_per_month_per_region_per_1000_inhabitants.csv")
cases_region_month = pd.read_csv("data/cases_per_month_per_region.csv")
total_cases_region_month = pd.read_csv("data/cases_per_month_per_region_per_1000_inhabitants.csv")

merged = dict()
merged_row = 0
for index, ivm_row in ivm_region_month_1000.iterrows():
    for row_index, ivm_row_value in ivm_row.items():
        if row_index != "STATE":
            cfr_value = cfr_region_month.loc[cfr_region_month["STATE"] == ivm_row["STATE"]][row_index].values[0]
            cases_per_1000_value = cases_region_month_1000.loc[cases_region_month_1000["STATE"] == ivm_row["STATE"]][row_index].values[0]
            merged[merged_row] = {"STATE": ivm_row["STATE"], "MONTH": row_index, "IVM": ivm_row_value, "CFR": cfr_value, "CASES_PER_1000": cases_per_1000_value}
            merged_row += 1

merged_df = pd.DataFrame.from_dict(merged, orient="index")

merged_df["IVM/CASE"] = merged_df["IVM"]/merged_df["CASES_PER_1000"]

merged_df.replace([np.inf, -np.inf], np.nan, inplace=True)
merged_df.dropna(subset=["IVM/CASE"], how="all")
#merged_df["MONTH"] = pd.to_datetime(merged_df["MONTH"])
merged_df = merged_df[merged_df["CFR"]!=0]

merged_df.to_csv("data/merged_dataset.csv")

#merged_df = merged_df[(merged_df['MONTH'] < '2021-01-01')]
#merged_df = merged_df[(merged_df['MONTH'] > '2021-04-01')]
#merged_df = merged_df[(merged_df['CASES'] > 10000)]
#merged_df = merged_df[merged_df['STATE'].isin(["BUENOS AIRES", "CAPITAL FEDERAL"])]

ivm_cfr_df = pd.DataFrame({'ivm':np.array(merged_df["IVM/CASE"]), 'cfr':np.array(merged_df["CFR"])})
ivm_cfr_df = ivm_cfr_df[ivm_cfr_df["cfr"]!=0]

r, p = scipy.stats.pearsonr(np.log(ivm_cfr_df["ivm"]), np.log(ivm_cfr_df["cfr"]))

fig = px.scatter(merged_df, x="IVM/CASE",
                 y="CFR",
                 title="CFR x IVM Purchases, " + 'Pearson R = '+ str(r) + ', p = ' + str(p),
                 color="STATE",
                 hover_data=["MONTH", "STATE"],
                 #text="STATE",
                 #size="CASES",
                 #trendline="ols",
                 #trendline_scope="overall",
                 trendline_options=dict(log_x=True, log_y=True),
                 log_x=True,
                 log_y=True,
                 #animation_frame="MONTH",
                 #animation_group="STATE",
                 #range_x=[1,5000],
                 #range_y=[0.001,0.2]
                 )
#fig.update_traces(textposition = "top center")
#fig.update_layout(transition = {'duration': 10000})

results = px.get_trendline_results(fig)
print(results)

fig.show()
