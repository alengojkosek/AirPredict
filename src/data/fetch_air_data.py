import pandas as pd
import requests
import json


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

df_arso.to_csv('raw_air_data.csv')