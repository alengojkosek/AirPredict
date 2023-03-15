import pandas as pd 
import numpy as np
import os

def get_latest_csv_version():
    # Find the latest version of the CSV file
    file_list = [f for f in os.listdir('.') if f.startswith('cleaned_arsopodatki_') and f.endswith('.csv')]
    if len(file_list) == 0:
        return 1
    latest_version = max([int(f.split('_')[-1].split('.')[0]) for f in file_list])
    return latest_version + 1

csv_versioning = get_latest_csv_version()

df = pd.read_csv('raw_arsopodatki_1.csv')

df['time'] = pd.to_datetime(df['time'])
df['datum_do'] = pd.to_datetime(df['datum_do'])
df['datum_od'] = pd.to_datetime(df['datum_od'])

df = df.replace('<2', np.nan)
df = df.replace('<1', np.nan)

df['pm10'] = df['pm10'].astype(float)

df = df.drop(columns=['o3', 'benzen', 'co', 'no2', 'so2', 'Unnamed: 0','ge_dolzina','ge_sirina','pm2.5', 'nadm_visina'])

df['pm10'] = df['pm10'].fillna(df['pm10'].mean())

# Drop string columns
df = df.select_dtypes(include=[float, int])

df.to_csv(f'cleaned_arsopodatki_{csv_versioning}.csv', index=False)

#print(df.isnull().sum())
#print(df.dtypes)
