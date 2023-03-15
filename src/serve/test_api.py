from flask import json
from api import app
from flask import json
import requests



def test_current_air():
    with app.test_client() as client:
    	response = client.get('/air/current/')
    	assert response.status_code == 200
    	data = response.json()
    	assert 'pm10' in data
    	assert isinstance(data['pm10'], int)

def test_current_weather():
    with app.test_client() as client:
    	response = client.get('/weather/current/')
    	assert response.status_code == 200
    	data = response.json()
    	assert 'temperature' in data
    	assert 'humidity' in data
    	assert 'wind_speed' in data
    	assert 'pressure' in data
    	assert isinstance(data['temperature'], float)
    	assert isinstance(data['humidity'], int)
    	assert isinstance(data['wind_speed'], float)
    	assert isinstance(data['pressure'], int)

def test_predict_air():
    with app.test_client() as client:
    	response = client.get('/air/predict/')
    	assert response.status_code == 200
    	data = response.json()
    	assert 'predictions' in data
    	predictions = data['predictions']
    	assert isinstance(predictions, list)
    	assert len(predictions) == 24
    	for p in predictions:
        	assert isinstance(p['datetime'], str)
        	assert isinstance(p['pm10'], float)

