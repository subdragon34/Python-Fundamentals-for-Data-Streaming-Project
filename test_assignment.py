from fastapi.testclient import TestClient

from api import app
from main import (
    EVENTS,
    EventValidationError,
    analyze_events,
    event_generator,
    occupancy_category,
    validate_event
)


client = TestClient(app)


def test_valid_event_is_accepted():
    event = {
        "Timestamp": "09:15",
        "Route": "AITU-Campus–Residence",
        "Bus": "B03",
        "Passengers": 12,
        "Speed_kmh": 35,
        "Status": "ON_ROUTE"
    }
    result = validate_event(event)
    assert result["Passengers"] == 12
    assert result["Speed_kmh"] == 35


def test_negative_passengers_are_rejected():
    event = {
        "Timestamp": "09:16",
        "Route": "AITU-Campus–Residence",
        "Bus": "B03",
        "Passengers": -1,
        "Speed_kmh": 35,
        "Status": "ON_ROUTE"
    }
    try:
        validate_event(event)
        assert False
    except EventValidationError as error:
        assert "Passengers must be a non-negative integer" in error.errors


def test_speed_above_limit_is_rejected():
    event = {
        "Timestamp": "09:17",
        "Route": "AITU-Campus–Residence",
        "Bus": "B03",
        "Passengers": 10,
        "Speed_kmh": 121,
        "Status": "ON_ROUTE"
    }
    try:
        validate_event(event)
        assert False
    except EventValidationError as error:
        assert "Speed_kmh must be between 0 and 120" in error.errors


def test_invalid_status_is_rejected():
    event = {
        "Timestamp": "09:18",
        "Route": "AITU-Campus–Residence",
        "Bus": "B03",
        "Passengers": 10,
        "Speed_kmh": 20,
        "Status": "MOVING"
    }
    try:
        validate_event(event)
        assert False
    except EventValidationError as error:
        assert "Status must be ON_ROUTE or STOPPED" in error.errors


def test_invalid_timestamp_is_rejected():
    event = {
        "Timestamp": "25:61",
        "Route": "AITU-Campus–Residence",
        "Bus": "B03",
        "Passengers": 10,
        "Speed_kmh": 20,
        "Status": "ON_ROUTE"
    }
    try:
        validate_event(event)
        assert False
    except EventValidationError as error:
        assert "Timestamp must use a valid HH:MM time" in error.errors


def test_decimal_passenger_count_is_rejected():
    event = {
        "Timestamp": "09:20",
        "Route": "AITU-Campus–Residence",
        "Bus": "B03",
        "Passengers": 12.5,
        "Speed_kmh": 20,
        "Status": "ON_ROUTE"
    }
    try:
        validate_event(event)
        assert False
    except EventValidationError as error:
        assert "Passengers must be a non-negative integer" in error.errors


def test_generator_yields_all_events_in_order():
    generated = list(event_generator(EVENTS))
    assert len(generated) == 10
    assert generated[0]["Timestamp"].strftime("%H:%M") == "08:00"
    assert generated[-1]["Timestamp"].strftime("%H:%M") == "08:09"


def test_occupancy_categories():
    assert occupancy_category(0) == "LOW"
    assert occupancy_category(10) == "LOW"
    assert occupancy_category(11) == "MEDIUM"
    assert occupancy_category(20) == "MEDIUM"
    assert occupancy_category(21) == "HIGH"
    assert occupancy_category(30) == "HIGH"
    assert occupancy_category(31) == "OVER_CAPACITY"


def test_analysis_results():
    result = analyze_events(EVENTS)
    assert result["average_passengers"] == 24.4
    assert result["maximum_passengers"] == 30
    assert result["stopped_events"] == 1
    assert result["busiest_minute"] == "08:09"
    assert result["busiest_bus"] == "B02"


def test_api_accepts_valid_event():
    response = client.post(
        "/events",
        json={
            "Timestamp": "08:05",
            "Route": "AITU-Campus–Residence",
            "Bus": "B02",
            "Passengers": 26,
            "Speed_kmh": 30,
            "Status": "ON_ROUTE"
        }
    )
    body = response.json()
    assert response.status_code == 200
    assert body["accepted"] is True
    assert body["validation_errors"] == []
    assert body["occupancy_category"] == "HIGH"


def test_api_returns_multiple_validation_errors():
    response = client.post(
        "/events",
        json={
            "Timestamp": "28:90",
            "Route": "AITU-Campus–Residence",
            "Bus": "B02",
            "Passengers": -5,
            "Speed_kmh": 150,
            "Status": "MOVING"
        }
    )
    body = response.json()
    assert response.status_code == 200
    assert body["accepted"] is False
    assert len(body["validation_errors"]) == 4
    assert body["occupancy_category"] is None
