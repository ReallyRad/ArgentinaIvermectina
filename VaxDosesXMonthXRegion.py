#extract number of vaccine doses per month per region per 1000 to vaxXMonthXRegionX1000.csv and cumulativeVaxXMonthXRegionX1000.csv
import pandas as pd

#fix encoding
def simplify(text):
	import unicodedata
	try:
		text = unicode(text, 'utf-8')
	except NameError:
		pass
	text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
	return str(text)

#read from government csv dataset
vax_df = pd.read_csv("data/datos_nomivac_covid19.csv", usecols = ["fecha_aplicacion", "jurisdiccion_residencia", ])
vax_region_month = dict()
population_df = pd.read_csv("data/population_region.csv")

#convert string date to python's datetime format
vax_df["fecha_aplicacion"] = pd.to_datetime(vax_df["fecha_aplicacion"])

for region in vax_df["jurisdiccion_residencia"].unique(): #for each region in the csv
  dates_dict = dict()
  if region == 'CABA':
    region = 'CAPITAL FEDERAL' #replace CABA by CAPITAL FEDERAL
  if region != "S.I.": #ignore entries where region is not specified
    for date in pd.date_range("2020-02-01", periods=15, freq="M"): #for each of the 15 months following February 2020
      #select the entries corresponding to the current region and the current month
      filtered_frame = vax_df.loc[(vax_df["jurisdiccion_residencia"] == region) &
                                  (vax_df["fecha_aplicacion"].between(date, date + pd.DateOffset(months=1)))]

      #get the vaccine doses
      new_vaccine_doses = filtered_frame.shape[0]

      #write the number of vaccine doses in our extracted dataset indexed by date
      dates_dict[date] = new_vaccine_doses

      #print to the console while extracting
      print("region : " + str(region))
      print("period : from " + str(date) + " to " + str(date + pd.DateOffset(months=1)))
      print("new vaccine doses : " + str(new_vaccine_doses))

      #extract population of the region to write the number of doses per 1000 population
      population = population_df[population_df.STATE == simplify(region).upper()]["Population"].values[0]
      dates_dict[date] = new_vaccine_doses / population * 1000

      vax_region_month[region] = dates_dict

#final formatting shenanigans
final_df = pd.DataFrame.from_dict(vax_region_month, orient="index")
final_df = final_df.reset_index()
final_df.rename(columns={'index': 'STATE'}, inplace=True)
final_df.STATE = [simplify(x).upper() for x in final_df.STATE]
#cfr_per_region_per_month.columns = [pd.to_datetime(x, errors='ignore').strftime("%M/%Y") for x in cfr_per_region_per_month.columns]

final_df.to_csv("data/vaxXMonthXRegionX1000.csv")
final_df.to_csv("data/cumulativeVaxXMonthXRegionX1000.csv")

