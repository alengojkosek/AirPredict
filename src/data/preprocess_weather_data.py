import pandas as pd
import requests
import json
import datetime
import os

df = pd.read_csv('raw_weather_data.csv')

df['time'] = pd.to_datetime(df['time'])

df.to_csv('preprocessed_weather_data.csv')
