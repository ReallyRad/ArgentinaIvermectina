import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

cases = pd.read_csv("casos confirmados.csv", encoding='utf-8')
# cases = pd.read_csv("covid19casos short.csv", encoding='latin-1')

ivm = pd.read_csv("IVMx1000.csv")

provinces = cases["carga_provincia_nombre"].unique()

cfrs = {}
for provincia in provinces :
  old_folks =  cases.loc[cases["edad"] > 65]
  old_folks_after_january = old_folks.loc[pd.to_datetime(old_folks["fecha_apertura"]) > pd.to_datetime("2020-12-01")]
  value_counts = old_folks_after_january.loc[old_folks_after_january["carga_provincia_nombre"] == provincia]["fallecido"].value_counts()
  if "SI" in value_counts.index:
    cfrs[provincia] = value_counts["SI"]/value_counts["NO"]

cfrs = pd.Series(cfrs)
ivm["sum"] = ivm.sum(axis = 1)
plt.scatter(ivm["sum"], cfrs)

ivm.sort_values(["STATE", "sum"])
cfrs = cfrs.sort_index()
for i,province in enumerate(provinces):
  plt.annotate(province, (ivm["sum"][i].item(), cfrs[i].item()))

lr = LinearRegression()
lr.fit(ivm["sum"].values.reshape(-1, 1), cfrs.values.reshape(-1, 1))
cfrs_pred = lr.predict(ivm["sum"].values.reshape(-1, 1))
plt.plot(ivm["sum"].values.reshape(-1, 1), cfrs_pred, color="red")
plt.show()
