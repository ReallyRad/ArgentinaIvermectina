import pandas as pd

def simplify(text):
	import unicodedata
	try:
		text = unicode(text, 'utf-8')
	except NameError:
		pass
	text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
	return str(text)

vax_df = pd.read_csv("data/datos_nomivac_covid19.csv", usecols = ["fecha_aplicacion", "jurisdiccion_residencia", ])
vax_region_month = dict()
population_df = pd.read_csv("data/population_region.csv")

vax_df["fecha_aplicacion"] = pd.to_datetime(vax_df["fecha_aplicacion"])

for region in vax_df["jurisdiccion_residencia"].unique():
  dates_dict = dict()
  if region == 'CABA':
    region = 'CAPITAL FEDERAL'
  elif region != "S.I.":
    for date in pd.date_range("2020-02-01", periods=15, freq="M"):
      filtered_frame = vax_df.loc[(vax_df["jurisdiccion_residencia"] == region) &
                                  (vax_df["fecha_aplicacion"].between(date, date + pd.DateOffset(months=1)))]

      new_vaccine_doses = filtered_frame.shape[0]

      dates_dict[date] = new_vaccine_doses

      print("region : " + str(region))
      print("period : from " + str(date) + " to " + str(date + pd.DateOffset(months=1)))
      print("new vaccine doses : " + str(new_vaccine_doses))
      population = population_df[population_df.STATE == simplify(region).upper()]["Population"].values[0]
      dates_dict[date] = new_vaccine_doses / population * 1000

      vax_region_month[region] = dates_dict

final_df = pd.DataFrame.from_dict(vax_region_month, orient="index")
final_df = final_df.reset_index()
final_df.rename(columns={'index': 'STATE'}, inplace=True)
final_df.STATE = final_df.STATE.replace("CABA", "CAPITAL FEDERAL")
final_df.STATE = [simplify(x).upper() for x in final_df.STATE]
#cfr_per_region_per_month.columns = [pd.to_datetime(x, errors='ignore').strftime("%M/%Y") for x in cfr_per_region_per_month.columns]

final_df.to_csv("data/vaxXMonthXRegionX1000.csv")
