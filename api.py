from fastapi import Body, FastAPI

from main import EventValidationError, occupancy_category, validate_event


app = FastAPI(
    title="AITU Campus Shuttle Event API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "AITU Campus Shuttle Event API",
        "endpoint": "POST /events"
    }


@app.post("/events")
def receive_event(event: dict = Body(...)):
    try:
        validated = validate_event(event)
    except EventValidationError as error:
        return {
            "accepted": False,
            "validation_errors": error.errors,
            "occupancy_category": None
        }

    return {
        "accepted": True,
        "validation_errors": [],
        "occupancy_category": occupancy_category(validated["Passengers"])
    }
