from app import app

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200

def test_shorten():
    client = app.test_client()
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    assert "short_code" in response.get_json()

def test_shorten_missing_url():
    client = app.test_client()
    response = client.post("/shorten", json={})
    assert response.status_code == 400
