import pandas as pd
import requests
import json

response = requests.get('https://arsoxmlwrapper.app.grega.xyz/api/air/archive')
data = json.loads(response.text)
df = pd.DataFrame()

for item in data:
    nested_json = json.loads(item["json"])
    postaja = nested_json["arsopodatki"]["postaja"]
    df = pd.concat([df, pd.DataFrame(postaja)], ignore_index=True)

df.to_csv('raw_arsopodatki.csv')