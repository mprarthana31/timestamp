from fastapi.testclient import TestClient
import pytest
from freezegun import freeze_time
from datetime import datetime, timezone
from app.main import app
import os

client = TestClient(app)

test_dates = [
    ("2015-02-15", {"unix": 1423958400000, "utc": "Sun, 15 Feb 2015, 00:00:00 UTC"}),
    ("2024-05-17", {"unix": 1715904000000, "utc": "Fri, 17 May 2024, 00:00:00 UTC"}),
    ("1451001600000", {"unix": 1451001600000, "utc": "Fri, 25 Dec 2015, 00:00:00 UTC"}),
]
invalid_dates = ["abc", "2015-14-09"]

freeze_time_dates = ["2012-04-08", "1985-07-15"]


@pytest.mark.parametrize("a", freeze_time_dates)
def test_api_null(a):
    with freeze_time(a):
        converted_date = datetime.strptime(a, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        response = client.get("/api")
        assert response.status_code == 200
        received = response.json()
        assert received["unix"] == datetime.timestamp(converted_date) * 1000
        assert received["utc"] == converted_date.strftime("%a, %d %b %Y, %H:%M:%S %Z")


@pytest.mark.parametrize("a,b", test_dates)
def test_api_value(a, b):
    # converted_date = datetime.strptime(a, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    response = client.get(f"/api/{a}")
    assert response.status_code == 200
    received = response.json()
    assert received["unix"] == b["unix"]
    assert received["utc"] == b["utc"]


@pytest.mark.parametrize("a", invalid_dates)
def test_api_invalid(a):
    response = client.get(f"/api/{a}")
    assert response.status_code == 200
    received = response.json()
    assert received["error"] == "Invalid Date"


def test_api_healthcheck():
    os.environ["GIT_SHA"] = "1234"

    response = client.get("/health")
    assert response.status_code == 200
    received = response.json()
    assert received["version"] == "1234"
