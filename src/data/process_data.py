import pandas as pd 
import numpy as np

df = pd.read_csv('raw_arsopodatki.csv')

df = df.replace('<2', np.nan)
df = df.replace('<1', np.nan)

df['pm2.5'] = df['pm2.5'].astype(float)
df['o3'] = df['o3'].astype(float)
df['pm10'] = df['pm10'].astype(float)
df['no2'] = df['no2'].astype(float)

df.drop(['Unnamed: 0'], axis=1, inplace=True)

df.drop(['so2'], axis=1, inplace=True)

df.interpolate(inplace=True)
df.dropna(inplace=True)

# Drop string columns
df = df.select_dtypes(include=[float, int])

df.to_csv('cleaned_arsopodatki.csv', index=False)

