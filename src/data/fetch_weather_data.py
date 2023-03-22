import pandas as pd
import requests
import json
import datetime


today = datetime.date.today()

three_days_advance = today + datetime.timedelta(days=3)

three_days_advance_string = three_days_advance.strftime('%Y-%m-%d')


forecast_response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude=46.42&longitude=15.87&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,pressure_msl,surface_pressure,precipitation,direct_radiation,diffuse_radiation,windspeed_10m&timezone=auto&start_date=2023-02-15&end_date={three_days_advance_string}') 

forecast_data = json.loads(forecast_response.text) 

# get the hourly weather data 
forecast_data = forecast_data['hourly'] 

df_forecast = pd.DataFrame(forecast_data) 

df_forecast.to_csv(raw_weather_data.csv)