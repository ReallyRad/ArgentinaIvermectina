import pandas as pd

#fecha_apertura
#fecha_internacion

#pour chaque région
#pour chaque mois
#divide confirmed cases by death counts (with time delay?)

dataframe = pd.read_csv("data/Covid19Casos.csv")
start_date = "2020-04-01"

dataframe["fecha_apertura"] = pd.to_datetime(dataframe["fecha_apertura"])

#grouper = dataframe.groupby([pd.Grouper(freq='M', level="fecha_apertura"), 'carga_provincia_nombre'])
cfrs_region_month = dict()

for region in dataframe["carga_provincia_nombre"].unique(): #for each region
  dates_dict = dict()

  for date in pd.date_range("2020-02-01", periods=15, freq="M"): #for each month in the specified range

    filtered_frame = dataframe.loc[(dataframe["carga_provincia_nombre"] == region) &
                              (dataframe["fecha_apertura"].between(date, date + pd.DateOffset(months=1))) &
                              (dataframe["clasificacion_resumen"] == "Confirmado") &
                              (dataframe["edad"] > 65)]

    confirmed_cases = filtered_frame.shape[0]
    deaths = filtered_frame[filtered_frame["fecha_fallecimiento"].notna()].shape[0]
    if(confirmed_cases > 0): CFR = deaths/confirmed_cases
    dates_dict[date] = CFR
    print("CFR between " + str(date) + " and " + str(date + pd.DateOffset(months=1)) + " in " + region + " is " + str(CFR))

  cfrs_region_month[region] = dates_dict
  cfrs_region_month_df = pd.DataFrame.from_dict(cfrs_region_month, orient="index")
  cfrs_region_month_df.index.name = "Region"
  cfrs_region_month_df.to_csv(region + ".csv")
  print("saved " + region + ".csv" )

pd.DataFrame.from_dict(cfrs_region_month, orient="index").to_csv("regions.csv")
