import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.app import app
from app.enums import EventStatus

@pytest.fixture
def client():
    """
    Fixture to provide a test client for FastAPI.
    """
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def future_deadline():
    """
    Returns a future timestamp as the event deadline
    """
    return (datetime.utcnow() + timedelta(days=1)).isoformat()

@pytest.fixture
def create_event(client, future_deadline):
    """
    Creates a new event using the API and returns its ID
    """
    response = client.post(
        "/events",
        json={"odds": 2.0, "deadline": future_deadline}
    )
    assert response.status_code == 200, f"Response: {response.json()}"
    return response.json()["id"]

def test_update_event_status_success(client, create_event):
    """
    Tests successful status update of an event.
    """
    event_id = create_event

    response = client.patch(f"/events/{event_id}?status=team1_win")
    assert response.status_code == 200
    data = response.json()
    assert data["event"]["status"] == EventStatus.TEAM1_WIN.value
    assert data["message"] == "The event was won by team 1"

    # Verify behavior when setting the same status again
    response = client.patch(f"/events/{event_id}?status=team1_win")
    assert response.status_code == 200
    data = response.json()
    assert data["event"]["status"] == EventStatus.TEAM1_WIN.value
    assert data["message"] == "The event was won by team 1"

def test_update_event_status_invalid_status(client, create_event):
    """
    Tests an attempt to set an invalid status.
    """
    event_id = create_event
    response = client.patch(f"/events/{event_id}?status=invalid_status")
    assert response.status_code == 422

    # Verify the error message returned by FastAPI
    detail = response.json()["detail"][0]["msg"]
    expected_messages = [
        "value is not a valid enumeration member; permitted: 'pending', 'team1_win', 'team1_loss'",
        "Input should be 'pending', 'team1_win' or 'team1_loss'"
    ]
    assert detail in expected_messages, f"Unexpected message: {detail}"

def test_update_event_status_not_found(client):
    """
    Tests status update for a non-existent event.
    """
    response = client.patch("/events/nonexistent-id?status=team1_win")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"
