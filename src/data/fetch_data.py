import pandas as pd
import requests
import json
import datetime
import os

def get_latest_csv_version():
    # Find the latest version of the CSV file
    file_list = [f for f in os.listdir('../data/raw/') if f.startswith('raw_arsopodatki_') and f.endswith('.csv')]
    if len(file_list) == 0:
        return 1
    latest_version = max([int(f.split('_')[-1].split('.')[0]) for f in file_list])
    return latest_version + 1

# get today's date
today = datetime.date.today()

# get the date 7 days ago
seven_days_ago = today - datetime.timedelta(days=7)
three_days_advance = today + datetime.timedelta(days=3)

# format today's date and 7 days ago as strings in the desired format
today_string = today.strftime('%Y-%m-%d')
seven_days_ago_string = seven_days_ago.strftime('%Y-%m-%d')
three_days_advance_string = three_days_advance.strftime('%Y-%m-%d')

# send the request and get the response 
historical_response = requests.get(f'https://archive-api.open-meteo.com/v1/archive?latitude=46.42&longitude=15.87&start_date=2023-02-15&end_date={seven_days_ago_string}&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,pressure_msl,surface_pressure,precipitation,direct_radiation,diffuse_radiation,windspeed_10m&timezone=auto') 
historical_data = json.loads(historical_response.text) 

# get the hourly weather data 
historical_data = historical_data['hourly'] 

# create a pandas DataFrame with the hourly weather data 
df_historical = pd.DataFrame(historical_data) 


# send the request and get the response 
forecast_response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude=46.42&longitude=15.87&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,pressure_msl,surface_pressure,precipitation,direct_radiation,diffuse_radiation,windspeed_10m&timezone=auto&start_date={seven_days_ago_string}&end_date={three_days_advance_string}') 
forecast_data = json.loads(forecast_response.text) 

# get the hourly weather data 
forecast_data = forecast_data['hourly'] 

# create a pandas DataFrame with the hourly weather data 
df_forecast = pd.DataFrame(forecast_data) 


arso_response = requests.get('https://arsoxmlwrapper.app.grega.xyz/api/air/archive')
arso_data = json.loads(arso_response.text)
df_arso = pd.DataFrame()

for item in arso_data:
    nested_json = json.loads(item["json"])
    postaja = nested_json["arsopodatki"]["postaja"]
    df_arso = pd.concat([df_arso, pd.DataFrame(postaja)], ignore_index=True)

# filter the rows where the value in the "merilno_mesto" column is "Ptuj"
df_arso = df_arso[df_arso["merilno_mesto"] == "Ptuj"]

df_arso = df_arso.sort_values(by='datum_do')
df_arso = df_arso.reset_index(drop=True)

# concatenate the dataframes vertically
df_meteo = pd.concat([df_historical, df_forecast], axis=0)

# reset the index of the combined dataframe
df_meteo = df_meteo.reset_index(drop=True)

# convert time and datum_do columns to datetime format
df_meteo['time'] = pd.to_datetime(df_meteo['time'])
df_arso['datum_do'] = pd.to_datetime(df_arso['datum_do'])
df_arso['datum_od'] = pd.to_datetime(df_arso['datum_od'])

# merge the two dataframes on the time and datum_do columns
merged_df = pd.merge(df_meteo, df_arso, left_on='time', right_on='datum_do')

csv_versioning = get_latest_csv_version()
merged_df.to_csv(f'../data/raw/raw_arsopodatki_{csv_versioning}.csv')
