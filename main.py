from datetime import datetime


EVENTS = [
    {
        "Timestamp": "08:00",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": 18,
        "Speed_kmh": 31,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:01",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": 22,
        "Speed_kmh": 28,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:02",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": 21,
        "Speed_kmh": 29,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:03",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": 25,
        "Speed_kmh": 27,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:04",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": 24,
        "Speed_kmh": 0,
        "Status": "STOPPED"
    },
    {
        "Timestamp": "08:05",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": 26,
        "Speed_kmh": 30,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:06",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": 23,
        "Speed_kmh": 32,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:07",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": 28,
        "Speed_kmh": 26,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:08",
        "Route": "AITU-Campus–Residence",
        "Bus": "B01",
        "Passengers": 27,
        "Speed_kmh": 25,
        "Status": "ON_ROUTE"
    },
    {
        "Timestamp": "08:09",
        "Route": "AITU-Campus–Residence",
        "Bus": "B02",
        "Passengers": 30,
        "Speed_kmh": 24,
        "Status": "ON_ROUTE"
    }
]


class EventValidationError(ValueError):
    def __init__(self, errors):
        self.errors = errors
        super().__init__("; ".join(errors))


def parse_timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Timestamp must be a string in HH:MM format")
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError as exc:
        raise ValueError("Timestamp must use a valid HH:MM time") from exc


def parse_passengers(value):
    if isinstance(value, bool):
        raise ValueError("Passengers must be a non-negative integer")
    if isinstance(value, int):
        number = value
    elif isinstance(value, str) and value.strip().lstrip("-").isdigit():
        number = int(value.strip())
    else:
        raise ValueError("Passengers must be a non-negative integer")
    if number < 0:
        raise ValueError("Passengers must be a non-negative integer")
    return number


def parse_speed(value):
    if isinstance(value, bool):
        raise ValueError("Speed_kmh must be a number between 0 and 120")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Speed_kmh must be a number between 0 and 120") from exc
    if not 0 <= number <= 120:
        raise ValueError("Speed_kmh must be between 0 and 120")
    return int(number) if number.is_integer() else number


def validate_event(event):
    if not isinstance(event, dict):
        raise EventValidationError(["Event must be a dictionary"])

    required_fields = (
        "Timestamp",
        "Route",
        "Bus",
        "Passengers",
        "Speed_kmh",
        "Status"
    )

    errors = []
    cleaned = {}

    for field in required_fields:
        if field not in event:
            errors.append(f"Missing required field: {field}")

    if errors:
        raise EventValidationError(errors)

    try:
        cleaned["Timestamp"] = parse_timestamp(event["Timestamp"])
    except ValueError as error:
        errors.append(str(error))

    route = event["Route"]
    if not isinstance(route, str) or not route.strip():
        errors.append("Route must be a non-empty string")
    else:
        cleaned["Route"] = route.strip()

    bus = event["Bus"]
    if not isinstance(bus, str) or not bus.strip():
        errors.append("Bus must be a non-empty string")
    else:
        cleaned["Bus"] = bus.strip()

    try:
        cleaned["Passengers"] = parse_passengers(event["Passengers"])
    except ValueError as error:
        errors.append(str(error))

    try:
        cleaned["Speed_kmh"] = parse_speed(event["Speed_kmh"])
    except ValueError as error:
        errors.append(str(error))

    status = event["Status"]
    if status not in {"ON_ROUTE", "STOPPED"}:
        errors.append("Status must be ON_ROUTE or STOPPED")
    else:
        cleaned["Status"] = status

    if errors:
        raise EventValidationError(errors)

    return cleaned


def format_event(event):
    return {
        **event,
        "Timestamp": event["Timestamp"].strftime("%H:%M")
    }


def event_generator(events):
    previous_timestamp = None
    for event in events:
        validated = validate_event(event)
        current_timestamp = validated["Timestamp"]
        if previous_timestamp is not None and current_timestamp < previous_timestamp:
            raise ValueError("Events are not in chronological order")
        previous_timestamp = current_timestamp
        yield validated


def process_stream(events):
    for event_number, raw_event in enumerate(events, start=1):
        try:
            validated = validate_event(raw_event)
            yield {
                "Event": event_number,
                "Passengers": validated["Passengers"],
                "Speed": validated["Speed_kmh"],
                "Status": validated["Status"],
                "Processed": "Yes",
                "Reason": "Valid event"
            }
        except EventValidationError as error:
            yield {
                "Event": event_number,
                "Passengers": raw_event.get("Passengers"),
                "Speed": raw_event.get("Speed_kmh"),
                "Status": raw_event.get("Status"),
                "Processed": "No",
                "Reason": "; ".join(error.errors)
            }


def occupancy_category(passengers):
    passengers = parse_passengers(passengers)
    if passengers <= 10:
        return "LOW"
    if passengers <= 20:
        return "MEDIUM"
    if passengers <= 30:
        return "HIGH"
    return "OVER_CAPACITY"


def analyze_events(events):
    count = 0
    passenger_sum = 0
    maximum_passengers = -1
    stopped_events = 0
    busiest_event = None

    for event in event_generator(events):
        count += 1
        passengers = event["Passengers"]
        passenger_sum += passengers

        if passengers > maximum_passengers:
            maximum_passengers = passengers
            busiest_event = event

        if event["Status"] == "STOPPED":
            stopped_events += 1

    if count == 0:
        return {
            "average_passengers": 0,
            "maximum_passengers": 0,
            "stopped_events": 0,
            "busiest_minute": None,
            "busiest_bus": None
        }

    return {
        "average_passengers": passenger_sum / count,
        "maximum_passengers": maximum_passengers,
        "stopped_events": stopped_events,
        "busiest_minute": busiest_event["Timestamp"].strftime("%H:%M"),
        "busiest_bus": busiest_event["Bus"]
    }


if __name__ == "__main__":
    print("Validated shuttle events")
    print("-" * 72)
    for index, event in enumerate(event_generator(EVENTS), start=1):
        clean_event = format_event(event)
        print(
            f'{index:02d} | {clean_event["Timestamp"]} | '
            f'{clean_event["Bus"]} | {clean_event["Passengers"]} passengers | '
            f'{clean_event["Speed_kmh"]} km/h | {clean_event["Status"]}'
        )

    print("\nStreaming simulation")
    print("-" * 72)
    for result in process_stream(EVENTS):
        print(
            f'Event {result["Event"]:02d} | passengers={result["Passengers"]} | '
            f'speed={result["Speed"]} | status={result["Status"]} | '
            f'processed={result["Processed"]} | reason={result["Reason"]}'
        )

    analysis = analyze_events(EVENTS)
    print("\nAnalysis")
    print("-" * 72)
    print(f'Average passenger count: {analysis["average_passengers"]:.1f}')
    print(f'Maximum passenger count: {analysis["maximum_passengers"]}')
    print(f'STOPPED events: {analysis["stopped_events"]}')
    print(f'Busiest minute: {analysis["busiest_minute"]}')
    print(f'Busiest bus: {analysis["busiest_bus"]}')
