import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()

region = "SANTA CRUZ"

cfr = pd.read_csv("CFR.csv", encoding='latin-1')
cfr["Date"] = pd.to_datetime(cfr["Date"])

ax1.bar(cfr["Date"], cfr[region], color ="red", label="CFR")
ax2 = ax1.twinx()

ivm = pd.read_csv("IVMx1000.csv")
index = ivm.index[ivm['STATE'] == region].tolist()[0]

ivm = ivm.iloc[: , 1:] #drop first column
ivm.columns = pd.to_datetime(ivm.columns)

fig.tight_layout()
ax2.plot(ivm.iloc[index], color = "yellow", label="ivm use")

ax1.legend(loc = 1)
ax2.legend(loc = 2)
plt.title(region)
plt.show()
