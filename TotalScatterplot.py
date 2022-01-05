import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import scipy.stats
import plotly_express as px
import plotly.graph_objects as go

ivm = pd.read_csv("data/IVMx1000.csv")
cfr_per_region = pd.read_csv("data/cfr_per_region.csv")
cases_per_region_per_month_per_1000 = pd.read_csv("data/cases_per_month_per_region_per_1000_inhabitants.csv")

cases_per_region_per_month_per_1000["sum"] = cases_per_region_per_month_per_1000.sum(axis = 1)
cases_per_region_per_month_per_1000 = cases_per_region_per_month_per_1000.set_index("STATE")

ivm["sum"] = ivm.sum(axis = 1)

cfr_per_region = cfr_per_region.sort_values(by="STATE")
cfr_per_region = cfr_per_region.set_index("STATE")

ivm = ivm.set_index("STATE")
cfr_per_region["IVM_TOTAL"] = ivm["sum"]
cfr_per_region["TOTAL_CASES_PER_1000"] = cases_per_region_per_month_per_1000["sum"]
cfr_per_region["IVM_PER_CASE"] = cfr_per_region["IVM_TOTAL"]/cfr_per_region["TOTAL_CASES_PER_1000"]
cfr_per_region = cfr_per_region.reset_index()

r, p = scipy.stats.pearsonr(np.log(cfr_per_region["IVM_PER_CASE"]), np.log(cfr_per_region["CFR"]))
#r, p = scipy.stats.pearsonr(ivm["sum"], cfr_per_region["CFR"])

fig = px.scatter(cfr_per_region,
                  x = "IVM_PER_CASE",
                  y = "CFR",
                  title="CFR x Total IVM Purchases per 1000 inhabitants, between March 2020 and May 2021 " + 'Pearson R = ' + str(r) + ', p = ' + str(p),
                  color = "STATE",
                  text="STATE",
                  size="TOTAL_CASES_PER_1000",
                  trendline="ols",
                  trendline_scope="overall",
                  trendline_options=dict(log_x=True, log_y=True),
                  log_x=True,
                  log_y=True,
                  )

fig.update_traces(textposition = "top center")

fig.show()
