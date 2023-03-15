from flask import json
from api import app


def test_current_air():
    with app.test_client() as client:
    	response = client.get('/air/current/')
    	assert response.status_code == 200

def test_current_weather():
    with app.test_client() as client:
    	response = client.get('/weather/current/')
    	assert response.status_code == 200

def test_predict_air():
    with app.test_client() as client:
    	response = client.get('/air/predict/')
    	assert response.status_code == 200
