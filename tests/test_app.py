import pytest
from urllib.parse import quote
from fastapi.testclient import TestClient

from src.app import app, activities


def test_get_activities():
    client = TestClient(app)
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data


def test_signup_and_unregister():
    activity_name = "Soccer Team"
    email = "pytest-user@example.com"

    activity_quoted = quote(activity_name, safe="")

    # ensure clean state
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    client = TestClient(app)

    # Sign up
    signup_resp = client.post(f"/activities/{activity_quoted}/signup", params={"email": email})
    assert signup_resp.status_code == 200
    assert email in activities[activity_name]["participants"]

    # Unregister
    unregister_resp = client.delete(f"/activities/{activity_quoted}/unregister", params={"email": email})
    assert unregister_resp.status_code == 200
    assert email not in activities[activity_name]["participants"]
