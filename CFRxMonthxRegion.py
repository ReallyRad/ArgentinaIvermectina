import pandas as pd

#fecha_apertura
#fecha_internacion

#pour chaque région
#pour chaque mois
#divide confirmed cases by death counts (with time delay?)

def simplify(text):
	import unicodedata
	try:
		text = unicode(text, 'utf-8')
	except NameError:
		pass
	text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
	return str(text)

dataframe = pd.read_csv("data/Covid19Casos.csv")
population_df = pd.read_csv("data/population_region.csv")
start_date = "2020-04-01"

dataframe["fecha_apertura"] = pd.to_datetime(dataframe["fecha_apertura"])

#grouper = dataframe.groupby([pd.Grouper(freq='M', level="fecha_apertura"), 'carga_provincia_nombre'])
cfrs_region_month = dict()

for region in dataframe["carga_provincia_nombre"].unique(): #for each region
  dates_dict = dict()

  for date in pd.date_range("2020-02-01", periods=15, freq="M"): #for each month in the specified range

    filtered_frame = dataframe.loc[(dataframe["carga_provincia_nombre"] == region) &
                              (dataframe["fecha_apertura"].between(date, date + pd.DateOffset(months=1))) &
                              (dataframe["clasificacion_resumen"] == "Confirmado")]

    confirmed_cases = filtered_frame.shape[0]
    deaths = filtered_frame[filtered_frame["fecha_fallecimiento"].notna()].shape[0]
    icu = filtered_frame[filtered_frame["cuidado_intensivo"] == "SI"].shape[0]
    ventilators = filtered_frame[filtered_frame["asistencia_respiratoria_mecanica"] == "SI"].shape[0]
    #population = population_df[population_df.STATE == simplify(region).upper()]["Population"].values[0]
    if(confirmed_cases > 0):
      CFR = deaths/confirmed_cases
      icu_rate = icu / confirmed_cases
      ventilator_rate = ventilators / confirmed_cases
    dates_dict[date] = icu_rate
    print("region : " + str(region))
    print("period : from " + str(date) + " to " + str(date + pd.DateOffset(months=1)))
    print("Deaths : " + str(deaths))
    print("CFR : " + str(CFR))
    print("Ventilators " + str(ventilators))
    print("Confirmed cases " + str(confirmed_cases))
    print("ICU " + str(icu))
    print("ICU rate " + str(icu_rate))
    print("")

  cfrs_region_month[region] = dates_dict
  cfrs_region_month_df = pd.DataFrame.from_dict(cfrs_region_month, orient="index")
  cfrs_region_month_df.index.name = "Region"

final_df = pd.DataFrame.from_dict(cfrs_region_month, orient="index")\

final_df = final_df.reset_index()
final_df.rename(columns={'index': 'STATE'}, inplace=True)
final_df.STATE = final_df.STATE.replace("CABA", "CAPITAL FEDERAL")
final_df.STATE = [simplify(x).upper() for x in final_df.STATE]
#cfr_per_region_per_month.columns = [pd.to_datetime(x, errors='ignore').strftime("%M/%Y") for x in cfr_per_region_per_month.columns]

final_df.to_csv("data/deaths.csv")
