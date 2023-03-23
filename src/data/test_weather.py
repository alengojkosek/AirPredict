import requests

def test_air_archive_url():
    url = 'https://api.open-meteo.com/v1/forecast?latitude=46.42&longitude=15.87'
    response = requests.get(url)
    assert response.status_code == 200
