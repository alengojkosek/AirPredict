import pandas as pd 
import numpy as np

df = pd.read_csv('raw_air_data.csv')

df['datum_do'] = pd.to_datetime(df['datum_do'])
df['datum_od'] = pd.to_datetime(df['datum_od'])

df = df.replace('<2', np.nan)
df = df.replace('<1', np.nan)

df['pm10'] = df['pm10'].astype(float)

df = df.drop(columns=['o3', 'benzen', 'co', 'no2', 'so2', 'Unnamed: 0','ge_dolzina','ge_sirina','pm2.5', 'nadm_visina'])

df['pm10'] = df['pm10'].fillna(df['pm10'].mean())

# Drop string columns
df = df.select_dtypes(include=[float, int])

df.to_csv('preprocessed_air_data.csv', index=False)

#print(df.isnull().sum())
#print(df.dtypes)
