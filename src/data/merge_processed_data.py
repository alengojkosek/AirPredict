import pandas as pd

df_meteo = pd.read_csv('raw_weather_data.csv')
df_arso = pd.read_csv('raw_air_data.csv')


# convert time and datum_do columns to datetime format
df_meteo['time'] = pd.to_datetime(df_meteo['time'])
df_arso['datum_do'] = pd.to_datetime(df_arso['datum_do'])
df_arso['datum_od'] = pd.to_datetime(df_arso['datum_od'])

# merge the two dataframes on the time and datum_do columns
merged_df = pd.merge(df_meteo, df_arso, left_on='time', right_on='datum_do')

merged_df.to_csv('merged_processed_data.csv')

