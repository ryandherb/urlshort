from fastapi.testclient import TestClient
from fastapi import status
from main import app

client = TestClient(app) 

def test_check_api_health():
    response = client.get("/health")
    assert response.json() == "ok"
    assert response.status_code == status.HTTP_200_OK
    
def test_should_create_shortened_url():
    url = "https://fastapi.tiangolo.com/"
    response = client.post("/shorten", json={"url": url})
    json = response.json()
    
    assert response.status_code == status.HTTP_201_CREATED
    assert "code" in json
    assert "short_url" in json
    
def test_should_redirect_to_original_url():
    url = "https://www.google.com"
    
    post_json = client.post("/shorten", json={"url": url}).json()
    
    response = client.get(f"/{post_json["code"]}", follow_redirects=False)
    
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert "https://www.google.com/" == response.headers.get("Location")

def test_should_reject_invalid_url():
    url = "notvalidurl"
    
    response = client.post("/shorten", json={"url": url})
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    
def test_should_reject_invalid_code():
    code = "abcdefghij"
    
    response = client.get(f"/{code}")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
def test_should_create_unique_indentifiers():
    url_1 = "https://www.google.com"
    url_2 = "https://www.github.com"
    
    response_1 = client.post("/shorten", json={"url": url_1})
    response_2 = client.post("/shorten", json={"url": url_2})
    
    assert response_1.status_code == status.HTTP_201_CREATED
    assert response_2.status_code == status.HTTP_201_CREATED
    
    assert response_1.json()["code"] != response_2.json()["code"]