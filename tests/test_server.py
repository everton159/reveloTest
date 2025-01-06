import pytest
import threading
import requests
from multiprocessing import Process
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import app

BASE_URL = "http://127.0.0.1:5000"

def start_server():
    app.run(debug=False, use_reloader=False)

@pytest.fixture(scope="module")
def test_server():
    process = Process(target=start_server)
    process.start()
    yield
    process.terminate()
    process.join()

def test_shorten_url(test_server):
    url = "https://www.google.com"
    response = requests.post(f"{BASE_URL}/shorten", json={"url": url})
    print("Test Shorten URL Response:", response.json())
    assert response.status_code == 201
    data = response.json()
    assert "short_url" in data

    short_url = data["short_url"]

    retrieve_response = requests.get(f"{BASE_URL}/retrieve/{short_url}")
    print("Test Retrieve URL Response:", retrieve_response.json())
    assert retrieve_response.status_code == 200
    retrieve_data = retrieve_response.json()
    assert retrieve_data["long_url"] == url

def test_invalid_url(test_server):
    response = requests.post(f"{BASE_URL}/shorten", json={})
    print("Test Invalid URL Response:", response.json())
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"] == "Invalid URL provided"

def test_redirect_url(test_server):
    url = "https://www.testurl.com"
    response = requests.post(f"{BASE_URL}/shorten", json={"url": url})
    print("Test Redirect URL Shorten Response:", response.json())
    assert response.status_code == 201
    data = response.json()
    short_url = data["short_url"]

    redirect_response = requests.get(f"{BASE_URL}/{short_url}", allow_redirects=False)
    print("Test Redirect URL Response:", redirect_response.headers)
    assert redirect_response.status_code == 302
    assert "Location" in redirect_response.headers
    assert redirect_response.headers["Location"] == url

def test_big_string_as_url(test_server):
    big_string = "https://www.testurl.com" + "a" * 10000  # A big string as a URL
    response = requests.post(f"{BASE_URL}/shorten", json={"url": big_string})
    print("Test Big String as URL Response:", response.json())
    assert response.status_code == 201
    data = response.json()
    assert "short_url" in data

def test_null_url(test_server):
    response = requests.post(f"{BASE_URL}/shorten", json={"url": None})
    print("Test Null URL Response:", response.json())
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert data["error"] == "Invalid URL provided"