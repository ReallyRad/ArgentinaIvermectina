import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()

region = "SANTA CRUZ"

cfr = pd.read_csv("data/CFR.csv", encoding='latin-1')
cfr["Date"] = pd.to_datetime(cfr["Date"])

ax1.bar(cfr["Date"], cfr[region], color ="red", label="CFR")
ax2 = ax1.twinx()

ivm = pd.read_csv("data/IVMx1000.csv")
index = ivm.index[ivm['STATE'] == region].tolist()[0]

ivm = ivm.iloc[: , 1:] #drop first column
ivm.columns = pd.to_datetime(ivm.columns)

fig.tight_layout()
ax2.plot(ivm.iloc[index], color = "yellow", label="ivm use")

casos = pd.read_csv("data/byRegion/casos confirmados Santa Cruz.csv")["fecha_apertura"]
casos = pd.to_datetime(casos)
casos.sort_values()
casos.value_counts().plot()

fallecimientos = pd.read_csv("data/byRegion/casos confirmados Santa Cruz.csv")["fecha_fallecimiento"]
fallecimientos = pd.to_datetime(fallecimientos)
fallecimientos.sort_values()
(fallecimientos.value_counts()*100).plot()

moving_cfr = fallecimientos.value_counts()/casos.value_counts()*10000
moving_cfr.plot()
# ax3 = ax1.twinx()<

ax1.legend(loc = 1)
ax2.legend(loc = 2)
plt.title(region)
plt.show()
