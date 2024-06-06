from fastapi.testclient import TestClient
import pytest
from freezegun import freeze_time
from datetime import datetime, timezone
from app.main import app

client = TestClient(app)

test_dates = ["2015-02-15", "2024-05-17", "1965-01-17"]
invalid_dates = ["abc", "2015-14-09"]

@pytest.mark.parametrize("a", test_dates)
def test_api_null(a):
    with freeze_time(a):
        converted_date = datetime.strptime(a,'%Y-%m-%d').replace(tzinfo= timezone.utc)
        response = client.get("/api")
        assert response.status_code == 200
        received = response.json()
        assert received["unix"] == datetime.timestamp(converted_date)*1000
        assert received["utc"] == converted_date.strftime('%a, %d %b %Y, %H:%M:%S %Z')

@pytest.mark.parametrize("a", test_dates)
def test_api_value(a):
    
    converted_date = datetime.strptime(a,'%Y-%m-%d').replace(tzinfo= timezone.utc)
    response = client.get(f"/api/{a}")
    assert response.status_code == 200
    received = response.json()
    assert received["unix"] == datetime.timestamp(converted_date)*1000
    assert received["utc"] == converted_date.strftime('%a, %d %b %Y, %H:%M:%S %Z')

@pytest.mark.parametrize("a", invalid_dates)
def test_api_invalid(a):
    
    response = client.get(f"/api/{a}")
    assert response.status_code == 200
    received = response.json()
    assert received["error"] == "Invalid Date"