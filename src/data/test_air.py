from api import app

def test_air_archive_url():
    with app.test_client() as client:
        url = 'https://arsoxmlwrapper.app.grega.xyz/api/air/archive'
        response = client.get(url)
        assert response.status_code == 200
