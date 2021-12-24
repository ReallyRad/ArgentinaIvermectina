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
    region_frame = dataframe[dataframe["carga_provincia_nombre"] == region] #filter by region
    region_date_frame = region_frame[region_frame["fecha_apertura"].between(date, date+pd.DateOffset(months = 1))] #filter by date

    datetime = pd.to_datetime("2020-03-05")
    region_date_frame_confirmed = region_date_frame[region_frame["clasificacion_resumen"] == "Confirmado"]  # filter only confirmed
    confirmed_cases = region_date_frame_confirmed.shape[0]
    deaths = region_date_frame_confirmed[region_date_frame_confirmed["fecha_fallecimiento"].notna()].shape[0]
    if(confirmed_cases > 0): CFR = deaths/confirmed_cases
    dates_dict[date] = CFR
    print("CFR between " + str(date) + " and " + str(date + pd.DateOffset(months=1)) + " in " + region + " is " + str(CFR))

  cfrs_region_month[region] = dates_dict
  cfrs_region_month_df = pd.DataFrame.from_dict(cfrs_region_month, orient="index")
  cfrs_region_month_df.index.name = "Region"
  cfrs_region_month_df.to_csv(region + ".csv")
  print("saved " + region + ".csv" )

pd.DataFrame.from_dict(cfrs_region_month, orient="index").to_csv("regions.csv")
