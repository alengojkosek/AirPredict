from api import app

def test_weather_url():
    with app.test_client() as client:
        url = 'https://api.open-meteo.com/v1/forecast?latitude=46.42&longitude=15.87'
        response = client.get(url)
        assert response.status_code == 200
