import datetime
import json
import os
import pickle

import pandas as pd
import requests
from flask import Flask, jsonify

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


with open('models/LG_model_3.pkl', 'rb') as f:
    model = pickle.load(f)

# get today's date
today = datetime.date.today()

# get the date 7 days ago
seven_days_ago = today - datetime.timedelta(days=7)
three_days_advance = today + datetime.timedelta(days=3)
one_day_advance = today + datetime.timedelta(days=1)
two_day_advance = today + datetime.timedelta(days=2)

# format today's date and 7 days ago as strings in the desired format
today_string = today.strftime('%Y-%m-%d')
seven_days_ago_string = seven_days_ago.strftime('%Y-%m-%d')
three_days_advance_string = three_days_advance.strftime('%Y-%m-%d')
one_day_advance_string = one_day_advance.strftime('%Y-%m-%d')
two_day_advance_string = two_day_advance.strftime('%Y-%m-%d')

three_days = three_days_advance.strftime('%d.%m.%Y')
one_days = one_day_advance.strftime('%d.%m.%Y')
two_days = two_day_advance.strftime('%d.%m.%Y')


@app.route('/air/current/', methods=['GET'])
def current_air():
    # make API request for all data
    arso_response = requests.get('https://arsoxmlwrapper.app.grega.xyz/api/air/latest')
    arso_data = json.loads(arso_response.text)
    # create DataFrame from API response
    arso_ptuj = arso_data['stations']
    # create DataFrame from JSON data
    df_arso = pd.DataFrame(arso_ptuj)

    # filter the rows where the value in the "station" column is "Ptuj"
    df_arso = df_arso[df_arso["station"] == "Ptuj"]
    response = {'pm10': df_arso['pm10'].tolist()}

    return json.dumps(response)

@app.route('/weather/current/', methods=['GET'])
def current_weather():
    now = datetime.datetime.now()
    current_hour = now.hour

    forecast_response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude=46.42&longitude=15.87&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,pressure_msl,surface_pressure,precipitation,direct_radiation,diffuse_radiation,windspeed_10m&timezone=auto&start_date={today_string}&end_date={today_string}')
    forecast_data = json.loads(forecast_response.text)
    current_hour_data = forecast_data['hourly']
    temperature = current_hour_data['temperature_2m'][current_hour]
    humidity = current_hour_data['relativehumidity_2m'][current_hour]
    wind_speed = current_hour_data['windspeed_10m'][current_hour]
    pressure = current_hour_data['pressure_msl'][current_hour]



    response = {
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'pressure': pressure
    }
    return jsonify(response)


@app.route('/air/predict/', methods=['GET'])
def predict_air():
    # send the request and get the response
    forecast_response = requests.get(
        f'https://api.open-meteo.com/v1/forecast?latitude=46.42&longitude=15.87&hourly=temperature_2m,relativehumidity_2m,dewpoint_2m,apparent_temperature,pressure_msl,surface_pressure,precipitation,direct_radiation,diffuse_radiation,windspeed_10m&timezone=auto&start_date={one_day_advance_string}&end_date={three_days_advance_string}')
    forecast_data = json.loads(forecast_response.text)

    # get the hourly weather data
    forecast_data = forecast_data['hourly']

    # create a pandas DataFrame with the hourly weather data
    df_forecast = pd.DataFrame(forecast_data)

    # Remove duplicates and keep only one value for each date
    df_forecast['date'] = pd.to_datetime(df_forecast['time']).dt.date
    df_forecast = df_forecast.groupby('date').first().reset_index()
    df_forecast.drop(['time', 'date'], axis=1, inplace=True)

    # Make the predictions
    y_pred = model.predict(df_forecast)

    # Format the predictions into a dictionary
    predictions = [
        {'date': one_days, 'value': round(y_pred[0], 2)},
        {'date': two_days, 'value': round(y_pred[1], 2)},
        {'date': three_days, 'value': round(y_pred[2], 2)}
    ]

    # Return the predictions as a JSON response
    return jsonify(predictions)


@app.route('/air/history/', methods=['GET'])
def history_air():
    # check if CSV file exists
    if os.path.exists('arso_cache.csv'):
        # load CSV into DataFrame
        df_arso = pd.read_csv('arso_cache.csv')
        # convert "datum_do" column to datetime format
        df_arso['datum_do'] = pd.to_datetime(df_arso['datum_do'])
        df_arso = df_arso.sort_values(by='datum_do', ascending=False).reset_index(drop=True)
        df_arso.drop("Unnamed: 0", axis=1, inplace=True)

    else:
        # make API request for all data
        arso_response = requests.get('https://arsoxmlwrapper.app.grega.xyz/api/air/archive')
        arso_data = json.loads(arso_response.text)
        # create DataFrame from API response
        df_arso = pd.DataFrame()
        for item in arso_data:
            nested_json = json.loads(item["json"])
            postaja = nested_json["arsopodatki"]["postaja"]
            df_arso = pd.concat([df_arso, pd.DataFrame(postaja)], ignore_index=True)
        # filter the rows where the value in the "merilno_mesto" column is "Ptuj"
        df_arso = df_arso[df_arso["merilno_mesto"] == "Ptuj"]
        # convert "datum_do" column to datetime format
        df_arso['datum_do'] = pd.to_datetime(df_arso['datum_do'])
        # sort DataFrame by "datum_do" column and reset index
        df_arso = df_arso.sort_values(by='datum_do', ascending=False).reset_index(drop=True)
        # save DataFrame to CSV file
        df_arso.to_csv('arso_cache.csv')

    # slice the last 10 rows of the sorted DataFrame
    df_arso_last_10 = df_arso.iloc[-10:]

    # extract the pm10 values from the sliced DataFrame
    pm10_history = df_arso_last_10['pm10'].tolist()

    # create the response dictionary
    response = {'pm10_history': pm10_history}

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=44933, debug=True)
