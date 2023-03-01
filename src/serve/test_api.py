from flask import json
from api import app


def test_api_running():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_api_404():
    with app.test_client() as client:
        response = client.get('/nonexistent/route')
        assert response.status_code == 404