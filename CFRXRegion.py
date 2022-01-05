import pandas as pd

cases = pd.read_csv("data/Covid19Casos.csv")
provinces = cases["carga_provincia_nombre"].unique()

cfrs = {}
for provincia in provinces :
  cases = cases[cases["clasificacion_resumen"] == "Confirmado"]
  value_counts = cases.loc[cases["carga_provincia_nombre"] == provincia]["fallecido"].value_counts()
  if "SI" in value_counts.index:
    cfrs[provincia] = value_counts["SI"]/value_counts["NO"]
    print ("CFR in " + provincia + " is " + str(cfrs[provincia]))

cfrs = pd.Series(cfrs)
cfrs.to_csv("data/cfr_per_region.csv")
