import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_invalid_short_url():
    response = client.get("/non_existent_short_url")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Short url does not exist'}


def test_url_shortener_with_correct_url():
    response = client.post("/shorten_url/", json.dumps({"url": "http://www.facebook.com"}))
    assert response.status_code == 200
    assert response.json()['short_url'] == 'smaller_url_as2hruy'


def test_url_shortener_with_incorrect_url():
    response = client.post("/shorten_url/", json.dumps({"url": "http:www.facebook.com"}))
    assert response.status_code == 400
    assert response.json() == {'detail':"The url is invalid"}

# TODOs- test the db, which will require mocking; Test the uniqueness of short url,
