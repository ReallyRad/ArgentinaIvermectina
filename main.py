import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#pd.read_csv("covid19casos short.csv")["fecha_fallecimiento"].value_counts().plot()



df = pd.read_csv("fallecimientos.csv")["fecha_fallecimiento"]
df = pd.to_datetime(df)
# df.sort_values(by='fecha_fallecimiento')
#df.value_counts().plot()


prescriptions = pd.read_csv("Argentine - Quantité région.csv")
prescriptions.loc[prescriptions["STATE"] == "LA PAMPA"]
prescriptions = prescriptions.iloc[: , 1:] #drop first column
prescriptions.columns = pd.to_datetime(prescriptions.columns)
prescriptions.iloc[0].plot.bar()
plt.show()



# to remove all non deaths
# df = pd.read_csv("Covid19Casos.csv")
# df = df[df["fecha_fallecimiento"].notna()]
# df.to_csv("fallecimientos.csv")
